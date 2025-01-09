import logging
import requests
from botenv import Env

from botsacflow.exceptions import SacflowErrorResponse


class Sacflow(Env):

    def __init__(self):
        """
        A class for interacting with the Sacflow API to send WhatsApp messages.
        """
        super().__init__(
            'SACFLOW',
            'API_TOKEN COOKIE'.split()
        )
        self.url = "https://api.sacflow.io/api/send-text"
        self.headers = {
            "cookie": self.credentials['COOKIE'],
            "authorization": self.credentials['API_TOKEN'],
            "Content-Type": "application/json"
        }

        self.payload = {
            "from": "BOT",
            "accountId": None,
            "tagId": None,
            "queueId": None,
            "whatsappId": None,
            "message": "",
            "contact": {
                "name": "Bot",
                "phone": ""
            },
            "isPrivate": False,
            "messageTimeout": 120,
            "document": {
                "url": '',
                "fileName": "report",
                "caption": "file"
            }

        }

    def send_msg_to_number(
            self,
            number,
            msg,
            whatsappId: int | None = None,
            tagId: int | None = None,
            queueId: int | None = None,
            file_url: str | None = None,
            accountId: int | None = None
            ):
        self.payload.update({'accountId': accountId})
        self.payload.update({'tagId': tagId})
        self.payload.update({'queueId': queueId})
        self.payload.update({'message': msg})
        self.payload.update({'whatsappId': whatsappId})
        self.payload.update({'contact': {
            "name": "Bot",
            "phone": str(number)
        }})
        self.payload.update({'document': {
            "url": file_url,
            "fileName": "report",
            "caption": "file"
        }})
        logging.info(self.payload)
        response = requests.request(
            "POST",
            self.url,
            json=self.payload,
            headers=self.headers
        )
        ret = response.json()
        logging.info(ret)
        if 'error' in ret:
            raise SacflowErrorResponse(
                f"Ocorreu um error na requisição: {ret}"
            )
        return ret


if __name__ == '__main__':
    sac = Sacflow()
    sac.send_msg_to_number(
        '5511123456789',
        "hi there! What's up?",
        1,
        2,
        3,
        accountId=4
    )
