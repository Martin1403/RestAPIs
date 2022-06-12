import os
import click
import shutil

from graphqlflaskapp.api.models import Job, Company, db
from graphqlflaskapp.api.dal import job_company_dal

# FOLDERS CONFIG
BASE = os.path.abspath(os.path.join(os.path.dirname(__name__), "graphqlflaskapp"))
DATABASE_FOLDER = os.path.join(BASE, "database")
os.makedirs(DATABASE_FOLDER, exist_ok=True)


@click.command("test-dal")
def dal_adapter():
    """Testing data access layer 'flask test-dal'"""
    with job_company_dal() as jcl:
        jobs = jcl.get_all_jobs()

    with job_company_dal() as jcl:
        job = jcl.get_job_by_id(id=jobs[0]["id"])

    with job_company_dal() as jcl:
        company = jcl.get_company_id(id=job["companyId"])

    with job_company_dal() as jcl:
        company_with_jobs = jcl.get_company_id_with_jobs(id=job["companyId"])

    with job_company_dal() as jcl:
        job = jcl.create_job(dict(
            companyId=job["companyId"],
            title="Senior Web Developer",
            description="Mulesoft API Development.Salesforce development."))

    click.echo("Test dal ok...")


@click.command("test-db")
def test_db():
    """Testing database 'flask test-db'"""
    db.create_all()

    for job in Job.query.all():
        db.session.delete(job)
    db.session.commit()
    db.session.flush()

    for company in Company.query.all():
        db.session.delete(company)
    db.session.commit()
    db.session.flush()

    company1 = Company(name="Apple", description="Tech Company.")
    company2 = Company(name="Microsoft", description="Software Company.")

    db.session.add_all([company1, company2])
    db.session.commit()
    db.session.flush()

    company1 = Company.query.filter_by(name=company1.name).first()

    job1 = Job(**dict(
        companyId=company1.id,
        title="Python Software Engineer",
        description="AI & Data Analytics division is working on interesting..."))

    job2 = Job(companyId=company1.id,
               title="Junior SW Developer",
               description="A Junior Software Application Developer works in a team of \
               engineers responsible for developing software")

    job3 = Job(companyId=company1.id,
               title="AI developer",
               description="AI & Data Analytics division is working on interesting projects for \
               some of the most recognized companies.")

    db.session.add_all([job1, job2, job3])
    db.session.commit()
    db.session.flush()

    job4 = Job(title="CSS developer",
               description="CSS & AI & Data Analytics division is working on interesting projects for \
               some of the most recognized companies.")
    job4.add_company = company2
    db.session.add(job4)
    db.session.commit()
    db.session.flush()

    click.echo("Test db ok...")


@click.command("init-db")
def init_db():
    """Recreate database flask init-db"""
    shutil.rmtree(DATABASE_FOLDER, ignore_errors=True)
    os.makedirs(DATABASE_FOLDER, exist_ok=True)
    db.create_all()

    click.echo("Initialize ok...")
