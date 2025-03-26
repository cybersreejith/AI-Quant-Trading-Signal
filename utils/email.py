import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from email.mime.application import MIMEApplication
from typing import List, Optional
from config.settings import SMTP_SERVER, SMTP_PORT, SMTP_USERNAME, SMTP_PASSWORD, EMAIL_SENDER
from utils.logger import setup_logger

logger = setup_logger(__name__)

def send_email(
    recipients: List[str],
    subject: str,
    body: str,
    attachments: Optional[List[str]] = None
) -> bool:
    """
    发送邮件
    :param recipients: 收件人列表
    :param subject: 邮件主题
    :param body: 邮件正文
    :param attachments: 附件列表
    :return: 是否发送成功
    """
    try:
        # 创建邮件对象
        msg = MIMEMultipart()
        msg['From'] = EMAIL_SENDER
        msg['To'] = ', '.join(recipients)
        msg['Subject'] = subject
        
        # 添加正文
        msg.attach(MIMEText(body, 'plain'))
        
        # 添加附件
        if attachments:
            for file_path in attachments:
                with open(file_path, 'rb') as f:
                    part = MIMEApplication(f.read())
                    part.add_header(
                        'Content-Disposition',
                        'attachment',
                        filename=file_path.split('/')[-1]
                    )
                    msg.attach(part)
        
        # 发送邮件
        with smtplib.SMTP(SMTP_SERVER, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USERNAME, SMTP_PASSWORD)
            server.send_message(msg)
            
        logger.info(f"邮件已成功发送到: {', '.join(recipients)}")
        return True
        
    except Exception as e:
        logger.error(f"发送邮件时出错: {str(e)}")
        return False 