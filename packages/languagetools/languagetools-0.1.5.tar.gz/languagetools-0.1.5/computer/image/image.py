import requests

class Image:
    def __init__(self, computer):
        self.computer = computer

    def generate(self, prompt: str):
        return self.computer.ai.cloud("create_image", {"prompt": prompt})

    def upscale(self, image_url: str):
        try:
            response = requests.head(image_url)
            if response.status_code != 200:
                print("This accepts URLs, so remember to run `lt files upload <path>` to upload the image first.")
        except:
            print("This accepts URLs, so remember to run `lt files upload <path>` to upload the image first.")
        return self.computer.ai.cloud("upscale_image", {"image": image_url})

    def restore(self, image_url: str):
        try:
            response = requests.head(image_url)
            if response.status_code != 200:
                print("This accepts URLs, so remember to run `lt files upload <path>` to upload the image first.")
        except:
            print("This accepts URLs, so remember to run `lt files upload <path>` to upload the image first.")
        return self.computer.ai.cloud("restore_image", {"image": image_url})
