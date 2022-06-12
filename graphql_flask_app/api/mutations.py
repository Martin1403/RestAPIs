from ariadne import MutationType

from graphqlflaskapp.api.dal import job_company_dal


mutation = MutationType()


@mutation.field("CreateJob")
def create_job(*_, input):
    with job_company_dal() as jcl:
        return jcl.create_job(input)


@mutation.field("CreateCompany")
def create_job(*_, input):
    with job_company_dal() as jcl:
        return jcl.create_company(input)
