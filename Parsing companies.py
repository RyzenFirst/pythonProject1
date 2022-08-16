columns=['name','company_business','description', 'number_employees', 'business_sector']
df = pd.DataFrame([['d','Nothing','Nothing',123,'Nithing']],columns=columns)
df.drop(0,inplace=True)
def converting_numbers(number):
    string = ''
    for i in number.split(','):
        string = string + i
    return int(string)
print(1)

def parsing(i=number_page):
    global df
    r = requests.get(
        f'https://www.value.today/world-top-1000-companies-as-on-jan-2020?title=&field_headquarters_of_company_target_id=All&field_company_category_primary_target_id=All&field_stock_exchange_lc_target_id=All&field_market_value_jan_2020_value=&page={i}',
        headers={'User-Agent': generate_user_agent()})
    page = bs(r.content, 'html.parser')
    companies = page.select('li[class="row well"]')
    if companies != []:
        for j in companies:
            information = pd.Series(
                {'name': company_name(j), 'company_business': company_business(j), 'description': description(j),
                 'number_employees': number_employees(j), 'business_sector': business_sector(j)})
            df = df.append(information, ignore_index=True)

def company_name(company):
    return company.select('h2[class="text-primary"] > a')[0].text


def number_employees(company):
    field = company.select(
        'div[class="clearfix col-sm-12 field field--name-field-employee-count field--type-integer field--label-inline"] > div')
    if field != []:
        return converting_numbers(field[1].text)
    else:
        return None


def company_business(company):
    z = company.select(
        'div[class="clearfix col-sm-12 category-button field field--name-field-company-category-primary field--type-entity-reference field--label-above"] > div')
    if z != []:
        business = []
        for i in z[1].select('div[class="field--item"]'):
            business.append(i.text)
        return business
    return None

def description(company):
    description = company.select('p')
    if description != []:
        return description[0].text
    else:
        return None

def business_sector(company):
    sector = company.select(
        'div[class="clearfix col-sm-12 field field--name-field-company-sub-category- field--type-entity-reference field--label-above"] > div > div')
    if sector != []:
        business_sector = []
        for i in sector:
            business_sector.append(i.text)
        return business_sector
    else:
        return None
with tqdm.tqdm(total=2046) as pbar:
    for number_page in range(2046):
        parsing(i=number_page)
        pbar.update(1)



