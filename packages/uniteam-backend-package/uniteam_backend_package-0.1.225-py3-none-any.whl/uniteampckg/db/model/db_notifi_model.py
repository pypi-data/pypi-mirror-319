from uniteampckg.db.model.db_base_model import BaseTableModel, Column
from datetime import datetime


class EmployeeDeviceLink(BaseTableModel):
    company_id: str = Column(foreign_key_table='company', foreign_key_column='company_id')
    employee_id: str = Column(foreign_key_table='employee', foreign_key_column='employee_id')
    device_id: str = Column()
    fcm_token: str = Column()
    last_used_at: datetime = Column()
    first_registered_at: datetime = Column()
    notification_allowed: bool = Column()
    video_allowed: bool = Column()
    mic_allowed: bool = Column()

class Notification(BaseTableModel):
    company_id:str = Column(foreign_key_table='company', foreign_key_column='company_id')
    notification_id:str = Column(primary_key=True)
    notification_type:str = Column()
    created_at:datetime = Column()
    in_app:bool = Column()
    push:bool = Column()
    email:bool = Column()
    sms:bool = Column()
    in_app_payload:dict = Column()
    email_template:dict = Column()
    email_payload:dict = Column()
    push_payload:dict = Column()
    sms_payload:dict = Column()
    ack_status:str = Column()
    add_to_email_summary:bool = Column()


class NotificationRecipientLink(BaseTableModel):
    company_id: str = Column(foreign_key_table='company', foreign_key_column='company_id')
    notification_id: str = Column(foreign_key_table='notification', foreign_key_column='notification_id')
    recipient_id: str = Column(foreign_key_table='employee', foreign_key_column='employee_id')
    ack_status: str = Column()



class PushNotificationLog(BaseTableModel):
    company_id: str = Column(foreign_key_table='company', foreign_key_column='company_id')
    notification_id: str = Column(foreign_key_table='notification', foreign_key_column='notification_id')
    recipient_id: str = Column(foreign_key_table='employee', foreign_key_column='employee_id')
    device_id: str = Column(foreign_key_table='employee_device_link', foreign_key_column='device_id')
    sent_at: datetime = Column()
    ack_status: str = Column()
    log_id: str = Column(primary_key=True)
    payload: dict = Column()



class EmailNotificationLog(BaseTableModel):
    company_id: str = Column(foreign_key_table='company', foreign_key_column='company_id')
    notification_id: str = Column(foreign_key_table='notification', foreign_key_column='notification_id')
    recipient_id: str = Column(foreign_key_table='employee', foreign_key_column='employee_id')
    template_id: str = Column()
    sent_at: datetime = Column()
    ack_status: str = Column()
    log_id: str = Column(primary_key=True)
    payload: dict = Column()


class SMSNotificationLog(BaseTableModel):
    company_id: str = Column(foreign_key_table='company', foreign_key_column='company_id')
    notification_id: str = Column(foreign_key_table='notification', foreign_key_column='notification_id')
    recipient_id: str = Column(foreign_key_table='employee', foreign_key_column='employee_id')
    template_id: str = Column()
    sent_at: datetime = Column()
    ack_status: str = Column()
    log_id: str = Column(primary_key=True)
    payload: dict = Column()