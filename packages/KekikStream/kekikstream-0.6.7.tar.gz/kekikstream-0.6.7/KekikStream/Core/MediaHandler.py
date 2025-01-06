# Bu araç @keyiflerolsun tarafından | @KekikAkademi için yazılmıştır.

from ..CLI            import konsol
from .ExtractorModels import ExtractResult
import subprocess, os

class MediaHandler:
    def __init__(self, title: str = "KekikStream", headers: dict = None):
        if headers is None:
            headers = {"User-Agent": "Mozilla/5.0 (Macintosh; Intel Mac OS X 10_14_5)"}

        self.headers = headers
        self.title   = title

    def play_media(self, extract_data: ExtractResult):
        if subprocess.check_output(['uname', '-o']).strip() == b'Android':
            return self.play_with_android_mxplayer(extract_data)

        if "Cookie" in self.headers or extract_data.subtitles:
            return self.play_with_mpv(extract_data)

        return self.play_with_vlc(extract_data)

    def play_with_vlc(self, extract_data: ExtractResult):
        try:
            vlc_command = ["vlc", "--quiet"]

            if self.title:
                vlc_command.extend([
                    f"--meta-title={self.title}",
                    f"--input-title-format={self.title}"
                ])

            if "User-Agent" in self.headers:
                vlc_command.append(f"--http-user-agent={self.headers.get('User-Agent')}")

            if "Referer" in self.headers:
                vlc_command.append(f"--http-referrer={self.headers.get('Referer')}")

            vlc_command.extend(
                f"--sub-file={subtitle.url}" for subtitle in extract_data.subtitles
            )
            vlc_command.append(extract_data.url)

            with open(os.devnull, "w") as devnull:
                subprocess.run(vlc_command, stdout=devnull, stderr=devnull, check=True)

        except subprocess.CalledProcessError as hata:
            konsol.print(f"[red]VLC oynatma hatası: {hata}[/red]")
            konsol.print({"title": self.title, "url": extract_data.url, "headers": self.headers})
        except FileNotFoundError:
            konsol.print("[red]VLC bulunamadı! VLC kurulu olduğundan emin olun.[/red]")
            konsol.print({"title": self.title, "url": extract_data.url, "headers": self.headers})

    def play_with_mpv(self, extract_data: ExtractResult):
        try:
            mpv_command = ["mpv", "--really-quiet"]

            if self.title:
                mpv_command.append(f"--force-media-title={self.title}")

            for key, value in self.headers.items():
                mpv_command.append(f"--http-header-fields={key}: {value}")

            mpv_command.extend(
                f"--sub-file={subtitle.url}" for subtitle in extract_data.subtitles
            )
            mpv_command.append(extract_data.url)

            with open(os.devnull, "w") as devnull:
                subprocess.run(mpv_command, stdout=devnull, stderr=devnull, check=True)

        except subprocess.CalledProcessError as hata:
            konsol.print(f"[red]mpv oynatma hatası: {hata}[/red]")
            konsol.print({"title": self.title, "url": extract_data.url, "headers": self.headers})
        except FileNotFoundError:
            konsol.print("[red]mpv bulunamadı! mpv kurulu olduğundan emin olun.[/red]")
            konsol.print({"title": self.title, "url": extract_data.url, "headers": self.headers})

    def play_with_android_mxplayer(self, extract_data: ExtractResult):
        paketler = [
            "com.mxtech.videoplayer.ad/.ActivityScreen",  # Free sürüm
            "com.mxtech.videoplayer.pro/.ActivityScreen"  # Pro sürüm
        ]

        for paket in paketler:
            try:
                android_command = [
                    "am", "start",
                    "-a", "android.intent.action.VIEW",
                    "-d", extract_data.url,
                    "-n", paket
                ]

                if self.title:
                    android_command.extend(["--es", "title", self.title])

                with open(os.devnull, "w") as devnull:
                    subprocess.run(android_command, stdout=devnull, stderr=devnull, check=True)

                return

            except subprocess.CalledProcessError as hata:
                konsol.print(f"[red]{paket} oynatma hatası: {hata}[/red]")
                konsol.print({"title": self.title, "url": extract_data.url, "headers": self.headers})
            except FileNotFoundError:
                konsol.print(f"Paket: {paket}, Hata: MX Player kurulu değil")
                konsol.print({"title": self.title, "url": extract_data.url, "headers": self.headers})