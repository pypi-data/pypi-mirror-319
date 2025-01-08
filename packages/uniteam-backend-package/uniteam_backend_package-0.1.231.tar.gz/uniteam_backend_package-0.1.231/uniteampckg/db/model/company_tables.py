from typing import List,Optional,Dict
from datetime import datetime
from uniteampckg.db.model.db_base_model import BaseTableModel,Column


class Company(BaseTableModel):
    company_id:Optional[str] = Column(primary_key=True)
    company_name: str = Column()
    admin_user_id: str = Column()
    admin_f_name: str = Column()
    admin_l_name: str = Column()
    admin_email: str = Column()
    finch_company_id: Optional[str] = Column()
    finch_access_key: Optional[str] = Column()
    hr_sync_status: Optional[str] = Column()
    hr_sync_date: Optional[str] = Column()
    number_of_employees: Optional[int] = Column()
    tango_customer_id: Optional[str] = Column()
    tango_account_id: Optional[str] = Column()
    unsynced_employees: Optional[List[str]] = Column()
    joined_at: datetime = Column()
    finch_connection_id: Optional[str] = Column()
    hr_conn_status: Optional[str] = Column()
    hris_enabled: Optional[bool] = Column()


class CompanyConfig(BaseTableModel):
    company_id: str = Column(primary_key=True, foreign_key_column='company_id', foreign_key_table='company')
    company_name: Optional[str] = Column()
    company_logo: Optional[str] = Column()
    color_pallete: Optional[str] = Column()
    subdomain: Optional[str] = Column()
    custom_domain: Optional[str] = Column()
    domain_settings: Optional[Dict] = Column()
    available_redeem_options: Optional[Dict] = Column()
    giftcard_vendors: Optional[Dict] = Column()
    maximum_spent: Optional[Dict] = Column()
    maximum_cart_value: Optional[Dict] = Column()
    employee_connection_info: Optional[Dict] = Column()
    employee_register_status_tracker: Optional[Dict] = Column()
    selected_departments: Optional[List[str]] = Column()
    auth_type: str = Column(default='EMAIL_PASS')
    sso_conn_id: Optional[str] = Column()
    is_all_emp_sync_enabled: Optional[bool] = Column()


