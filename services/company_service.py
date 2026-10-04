from dao.company_dao import CompanyDAO


def get_or_create_company(company_name):

    company_dao = CompanyDAO()

    company = company_dao.find_by_name(company_name)
    if company is not None:
        return company.id

    new_id = company_dao.insert(company_name)
    return new_id


if __name__ == "__main__":
    company_id = get_or_create_company("Amazon")
    print(f"Company ID: {company_id}")

    company_id_again = get_or_create_company("Amazon")
    print(f"Company ID (second call): {company_id_again}")