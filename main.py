from getting_links import LinksFetch
from scrap import Scraping
from bs import Bs4_Scaping, page_loggers
from excel_writer import excel_write


def find_num(num1, num2):
    if num1 != num2:
        max_num = max(num1, num2)
        return max_num
    else:
        return num1


BASE_URL = "https://extract.co/top-app-development-companies-in-uk"

while BASE_URL:
    main_page_links = LinksFetch(url=BASE_URL)
    m = main_page_links.getter_links(cls_name="company-name")
    for link in m:
        F_L = []
        FINAL_LIST = []
        TEMP_LIST = []
        b = Bs4_Scaping(url=link)
        company_name = b.get_name()

        TEMP_LIST.append(company_name['name'])
        TEMP_LIST.append(company_name['company_url'])
        TEMP_LIST.append(company_name['state'])
        TEMP_LIST.append(company_name['country'])

        breif = b.get_breif(cls_name="row", element="li")
        TE_LI = TEMP_LIST + breif
        exp = b.expertise()

        TE_LI.append(exp)

        industry = b.industry_focus()
        TE_LI.append(industry)
        review = b.reviews_reader()
        for c, re in enumerate(review):
            if c >= 1:
                TE_LI = [None for t in TE_LI]
                l = TE_LI + re
                F_L.append(l)
            else:
                l = TE_LI + re
                F_L.append(l)

        reviews_works_links = b.get_reviews_works()
        c = Scraping(url=reviews_works_links[0])
        returned_links_list = c.get_link(cls_name="btnmoreinfo")
        col = []
        for i in returned_links_list:
            obj = Bs4_Scaping(url=i)
            k = obj.check_hired_products()
            col.append(k)
        # print(F_L)
        final_list_len = len(F_L)
        review_list = len(col)
        max_number = find_num(final_list_len, review_list)

        for_for_loop = review_list - final_list_len

        if for_for_loop != 0:
            for extra_adds in range(final_list_len, review_list):
                l = [None for i in range(1, 20)]
                F_L.append(l)

        for c in range(len(col)):
            l = F_L[c] + col[c]
            FINAL_LIST.append(l)

        for single_line in FINAL_LIST:
            excel_write(write_list=single_line, file_name="uk")

    nex_link = main_page_links.getter_links(cls_name="pull-right")
    BASE_URL = nex_link[0]
    page_loggers(log_name="logger", text=f"{str(BASE_URL)} - COMPLETED")

