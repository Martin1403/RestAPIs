from ariadne import QueryType

from graphqlflaskapp.api.dal import job_company_dal


query = QueryType()


@query.field('jobs')
def get_all_jobs(*_):
    with job_company_dal() as jcd:
        return jcd.get_all_jobs()


@query.field("job")
def get_job_by_id(*_, id):
    with job_company_dal() as jcl:
        return jcl.get_job_by_id(id=id)


@query.field("company")
def get_company_by_id(*_, id):
    with job_company_dal() as jcl:
        return jcl.get_company_id_with_jobs(id=id)


