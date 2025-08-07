from dotenv import load_dotenv
import os
import logging
from mailer import Mailer
from suricata import SuricataAlertReader
import time
logging.basicConfig(level=logging.INFO, format='%(asctime)s - %(levelname)s - %(message)s')


def main():
    logging.info("Starting...")

    load_dotenv()

    logging.info("Loaded enviroment variables!")

    mailer_type = os.getenv("MAILER")
    username = os.getenv("USERNAME")
    password = os.getenv("PASSWORD")
    from_email = os.getenv("FROM")
    to_emails = os.getenv("TO").split(",")
    smtp_server = os.getenv("SMTP_SERVER")
    port = int(os.getenv("PORT"))
    polling_time = int(os.getenv("POLLING_TIME"))

    logging.info("Setting up mailer...")

    mailer = Mailer(mailer_type,port,smtp_server, username, password)

    logging.info("Setup mailer successfuly!")

    reader = SuricataAlertReader("/logs/eve.json")

    try:
        while True:
            alerts = reader.get_new_alerts()
            if len(alerts) == 0:
                time.sleep(polling_time)
                continue
            subject = f"[Suricata Alert] {len(alerts)} New Alert(s)"
            body = ["New Suricata alert(s) detected:\n"]
            for alert in alerts:
                a = alert["alert"]
                body.append(
                    f"- {a['signature']}\n"
                    f"  Source: {alert['src_ip']}:{alert['src_port']}\n"
                    f"  Destination: {alert['dest_ip']}:{alert['dest_port']}\n"
                    f"  Protocol: {alert['proto']}\n"
                    f"  Time: {alert['timestamp']}\n"
                )
                logging.info(f"ALERT: {alert['alert']['signature']}")
            for to_email in to_emails:
                mailer.send_message(from_email, to_email, subject, "\n".join(body))
            time.sleep(polling_time)
    finally:
        reader.close()

main()