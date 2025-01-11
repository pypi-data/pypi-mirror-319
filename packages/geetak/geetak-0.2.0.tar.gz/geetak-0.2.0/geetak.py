import platform
import click
import time
from datetime import datetime, timezone, timedelta
from threading import Timer
from rich.progress import Progress, TextColumn, BarColumn, TimeRemainingColumn
from rich_click import RichCommand, RichGroup
from rich import print
import ntplib
import os
import json
import rich_click as click

# Cross-platform HID library imports
if platform.system() == "Windows":
    import pywinusb.hid as hid # type: ignore
else:
    import hid

# Configure rich-click
click.rich_click.USE_RICH_MARKUP = True
click.rich_click.MAX_WIDTH = 100
click.rich_click.SHOW_ARGUMENTS = True
click.rich_click.SHOW_METAVARS_COLUMN = False
click.rich_click.GROUP_ARGUMENTS_OPTIONS = True


# Konstanta untuk USB Relay
USB_CFG_VENDOR_ID = 0x16c0
USB_CFG_DEVICE_ID = 0x05DF

# File konfigurasi untuk menyimpan offset zona waktu
CONFIG_FILE = "geetak_config.json"


class USBRelayController:
    def __init__(self, vendor_id, product_id):
        self.vendor_id = vendor_id
        self.product_id = product_id
        self.device = None
        self.report = None
        self.is_windows = platform.system() == "Windows"

    def connect(self):
        try:
            if self.is_windows:
                # Windows-specific: pywinusb.hid
                filter = hid.HidDeviceFilter(vendor_id=self.vendor_id, product_id=self.product_id)
                devices = filter.get_devices()
                if not devices:
                    raise Exception("Tidak ada perangkat HID yang ditemukan.")
                self.device = devices[0]
                self.device.open()
                self.get_report()
            else:
                # Cross-platform: hidapi
                self.device = hid.device()
                self.device.open(self.vendor_id, self.product_id)
                self.device.set_nonblocking(1)

            print("[bold green]Perangkat berhasil terhubung.[/bold green]")
        except Exception as e:
            print(f"Gagal menghubungkan perangkat: {e}")

    def get_report(self):
        if self.is_windows and self.device:
            reports = self.device.find_output_reports() + self.device.find_feature_reports()
            if reports:
                self.report = reports[0]
            else:
                print("[red]Tidak ada laporan yang ditemukan pada perangkat.[/red]")

    def is_device_available(self):
        try:
            if self.is_windows:
                # Check using pywinusb.hid
                filter = hid.HidDeviceFilter(vendor_id=self.vendor_id, product_id=self.product_id)
                devices = filter.get_devices()
                return len(devices) > 0
            else:
                # Check using hidapi
                device = hid.device()
                device.open(self.vendor_id, self.product_id)
                device.close()
                return True
        except Exception:
            return False

    def write(self, buffer):
        try:
            if self.is_windows:
                if self.report:
                    print(f"[yellow]Mengirim data ke perangkat (Windows): {buffer}[/yellow]")
                    self.report.send(raw_data=buffer)
                else:
                    print("[red]Tidak ada laporan yang tersedia untuk mengirim data.[/red]")
            else:
                buffer = [0x00] + buffer  # Add report ID (or 0x00 if not used)
                buffer += [0x00] * (9 - len(buffer))  # Ensure buffer matches report size
                print(f"[yellow]Mengirim data ke perangkat (macOS/Linux): {buffer}[/yellow]")
                self.device.write(buffer)
        except Exception as e:
            print(f"[red]Gagal mengirim data ke perangkat: {e}[/red]")

    def disconnect(self):
        if self.device:
            try:
                if self.is_windows:
                    if self.device.is_opened():
                        self.device.close()
                else:
                    self.device.close()
                print("[bold green]Perangkat berhasil terputus.[/bold green]")
            except Exception as e:
                print(f"[red]Gagal memutuskan perangkat: {e}[/red]")

    def trigger_relay(self, relay_number, duration=1):
        print(f"[bold cyan]Relay {relay_number} dihidupkan.[/bold cyan]")
        buffer_on = [0xFF, relay_number, 0, 0, 0, 0, 0, 1]
        self.write(buffer_on)

        def turn_off():
            print(f"[bold cyan]Relay {relay_number} dimatikan.[/bold cyan]")
            buffer_off = [0xFD, relay_number, 0, 0, 0, 0, 0, 1]
            self.write(buffer_off)
            self.disconnect()

        Timer(duration, turn_off).start()


def get_config():
    """Memuat konfigurasi dari file."""
    if os.path.exists(CONFIG_FILE):
        with open(CONFIG_FILE, "r") as file:
            return json.load(file)
    return {"timezone_offset": 0}  # Default ke UTC


def save_config(config):
    """Menyimpan konfigurasi ke file."""
    with open(CONFIG_FILE, "w") as file:
        json.dump(config, file)


def get_ntp_time():
    """Mengambil waktu UTC dari server NTP dan menyesuaikan dengan zona waktu yang dikonfigurasi."""
    try:
        ntp_client = ntplib.NTPClient()
        response = ntp_client.request('2.id.pool.ntp.org')
        # Gunakan datetime UTC dengan timezone
        utc_time = datetime.fromtimestamp(response.tx_time, tz=timezone.utc)

        # Sesuaikan dengan offset zona waktu
        config = get_config()
        timezone_offset = config.get("timezone_offset", 0)
        local_time = utc_time + timedelta(hours=timezone_offset)

        return local_time
    except Exception as e:
        print(f"Gagal mengambil waktu dari server NTP: {e}")
        # Gunakan waktu UTC dari sistem sebagai cadangan
        return datetime.now(tz=timezone.utc)



@click.group(cls=RichGroup)
def cli():
    """[bold blue]Geetak CLI[/bold blue] untuk mengontrol [bold green]USB relay[/bold green]."""
    pass


@cli.command(cls=RichCommand)
@click.argument("time_str", type=str)
@click.option("--offset", type=int, default=0, help="[cyan]Tambahan delay dalam milidetik (ms).[/cyan]")
def gas(time_str, offset):
    """
    Memulai [bold green]timer[/bold green] untuk mengaktifkan relay pada waktu tertentu.
    
    [yellow]TIME_STR[/yellow] harus dalam format [bold cyan]HH:MM:SS[/bold cyan].
    Gunakan [yellow]--offset[/yellow] untuk menambahkan delay tambahan dalam milidetik.
    """
    print("[bold green]Memulai timer...[/bold green]")
    try:
        # Ambil waktu NTP (timezone-aware)
        now = get_ntp_time()
        print(f"Waktu lokal saat ini (NTP): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")

        # Parsing waktu target dan buat timezone-aware
        target_time_naive = datetime.strptime(time_str, "%H:%M:%S").replace(
            year=now.year, month=now.month, day=now.day
        )
        target_time = target_time_naive.replace(tzinfo=now.tzinfo)

        # Tangani jika waktu target lebih awal dari waktu sekarang
        if target_time < now:
            target_time += timedelta(days=1)

        # Hitung delay
        delay = (target_time - now).total_seconds()

        # Tambahkan offset dalam milidetik (diubah ke detik)
        delay += offset / 1000.0

        print(f"Timer diatur untuk {target_time.strftime('%H:%M:%S %Z')} "
              f"(dalam {delay:.2f} detik, termasuk offset {offset} ms).")

        # Buat dan sambungkan ke relay
        controller = USBRelayController(USB_CFG_VENDOR_ID, USB_CFG_DEVICE_ID)
        controller.connect()

        # Progress bar setup
        with Progress(
            TextColumn("[progress.description]{task.description}"),
            BarColumn(),
            TimeRemainingColumn(),
        ) as progress:
            task = progress.add_task("Menunggu waktu target...", total=delay)
            while not progress.finished:
                time.sleep(0.1)
                progress.update(task, advance=0.1)

        # Atur relay setelah progress selesai
        controller.trigger_relay(1)

    except ValueError:
        print("Format waktu tidak valid. Gunakan format HH:MM:SS.")
    except Exception as e:
        print(f"Terjadi kesalahan: {e}")


@cli.command(cls=RichCommand)
def cekwaktu():
    """
    Menampilkan [bold green]waktu server NTP[/bold green] saat ini.
    """
    print("[bold blue]Menampilkan waktu NTP...[/bold blue]")
    try:
        now = get_ntp_time()
        print(f"Waktu lokal saat ini (NTP): {now.strftime('%Y-%m-%d %H:%M:%S %Z')}")
    except Exception as e:
        print(f"Gagal mengambil waktu dari NTP: {e}")


@cli.command(cls=RichCommand)
def cekalat():
    """
    Memeriksa apakah [bold green]perangkat USB relay[/bold green] tersedia.
    """
    print("[bold red]Memeriksa perangkat USB relay...[/bold red]")

    controller = USBRelayController(USB_CFG_VENDOR_ID, USB_CFG_DEVICE_ID)
    if controller.is_device_available():
        print("Perangkat USB relay tersedia.")
    else:
        print("Perangkat USB relay tidak tersedia.")


@cli.command(cls=RichCommand)
@click.argument("timezone_offset", type=int)
def ubahzona(timezone_offset):
    """
    Mengatur [bold green]zona waktu offset[/bold green] dalam jam (misalnya, [cyan]+7[/cyan] atau [cyan]-5[/cyan]).
    """
    print(f"[bold yellow]Zona waktu diatur ke {timezone_offset:+d} jam.[/bold yellow]")
    try:
        config = get_config()
        config["timezone_offset"] = timezone_offset
        save_config(config)
        print(f"Zona waktu diperbarui ke {timezone_offset:+d} jam.")
    except Exception as e:
        print(f"Gagal memperbarui zona waktu: {e}")


if __name__ == "__main__":
    cli()