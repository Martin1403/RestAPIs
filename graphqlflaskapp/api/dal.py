from contextlib import contextmanager

from graphqlflaskapp.api.models import db, Job, Company


class JobCompanyDAL(object):
    """DataAccessLayer"""

    def __init__(self, session):
        self.db = session

    def get_all_jobs(self):
        return [{**job.json(), **{"company": self.get_company_id(job.companyId)}} for job in Job.query.all()]

    def get_job_by_id(self, id):
        job = Job.query.filter_by(id=id).first()
        company = self.get_company_id(job.companyId)
        return {**job.json(), **{"company": company.json()}}

    @staticmethod
    def get_company_id(id):
        return Company.query.filter_by(id=id).first()

    def get_company_id_with_jobs(self, id):
        company = self.get_company_id(id)
        if company:
            company_jobs = [job.json() for job in Job.query.filter_by(companyId=company.id).all()]
            return {**company.json(), **{"jobs": company_jobs}}
        return None

    def create_job(self, kwargs):
        job = Job(**kwargs)
        self.db.session.add(job)
        self.db.session.commit()
        return self.get_job_by_id(id=job.id)

    def create_company(self, kwargs):
        company = Company(**kwargs)
        self.db.session.add(company)
        self.db.session.commit()
        return self.get_company_id_with_jobs(company.id)


@contextmanager
def job_company_dal():
    yield JobCompanyDAL(db)
