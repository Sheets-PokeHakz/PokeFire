import time
import os
import requests
from pydub import AudioSegment
from seleniumbase import Driver
import speech_recognition as sr


def download_audio(driver, download_button, file_path):

    download_link = driver.get_attribute(download_button, "href")
    buffer = requests.get(download_link)

    with open(file_path, "wb") as file:
        file.write(buffer.content)


def convert_mp3_to_wav(mp3_path, wav_path):

    sound = AudioSegment.from_mp3(mp3_path)
    sound.export(wav_path, format="wav")


def recognize_audio(wav_path):

    recognizer = sr.Recognizer()
    with sr.AudioFile(wav_path) as source:
        audio = recognizer.record(source)
    try:
        return recognizer.recognize_google(audio)
    except sr.UnknownValueError:
        return None


def solve_captcha(driver, id):

    url = f"https://verify.poketwo.net/captcha/{id}"
    captcha_box = "#recaptcha-anchor > div.recaptcha-checkbox-checkmark"
    audio_button = "#recaptcha-audio-button"
    download_button = "#rc-audio > div.rc-audiochallenge-tdownload > a"

    driver.uc_open_with_reconnect(url, 5)

    if driver.is_text_visible("Please verify to continue"):
        print("[!] Successfully bypassed Cloudflare")

        driver.uc_switch_to_frame("iframe[title='reCAPTCHA']")
        driver.uc_click(captcha_box)

        driver.uc_switch_to_frame(
            "iframe[title='recaptcha challenge expires in two minutes']"
        )
        driver.uc_click(audio_button)

        driver.uc_switch_to_frame(
            "iframe[title='recaptcha challenge expires in two minutes']"
        )
        audio_file_path = f"sound-{id}.mp3"
        wav_file_path = f"sound-{id}.wav"

        download_audio(driver, download_button, audio_file_path)
        convert_mp3_to_wav(audio_file_path, wav_file_path)

        text = recognize_audio(wav_file_path)

        os.remove(wav_file_path)
        os.remove(audio_file_path)

        if text:
            driver.type("#audio-response", text)
            driver.uc_click("#recaptcha-verify-button")

            if not driver.is_text_visible(
                "Multiple correct solutions required - please solve more.",
                selector="#rc-audio > div.rc-audiochallenge-error-message",
            ):
                driver.uc_click("#__next > div > div > button")
                print("[!] Completed the Captcha challenge")
                return True
            else:
                print("[?] Failed to solve Captcha. Retrying in 5 seconds...")
        else:
            print("[?] Failed to solve Captcha. Retrying in 5 seconds...")

    else:
        print("[?] Could not bypass Cloudflare. Retrying in 5 seconds...")

    time.sleep(5)
    return False


def verify(bot):

    while not bot.verified:
        driver = Driver(
            browser="Chrome",
            uc=True,
            headless2=True,
            incognito=True,
            do_not_track=True,
            undetectable=True,
        )

        if solve_captcha(driver, bot.user.id):
            bot.verified = True

        driver.quit()

    return True
