"""
Script to download DYD reports
"""

import sys
import urllib
import argparse
import requests
import yaml
import json

from parsel import Selector


CONFIG = {
    "mclass_baseurl": "https://mclass.amplify.com",
    "reports_path": "/reports/myReports",
    "dyd_api_path": "/reports/api/report/downloadyourdata",
    "reporting_login": "/reports/login",
}

DEFAULT_DATA = {
        "result": "download_your_data",
        "dyd_assessments": "7_32",
        "years": "20",
        "periods": "20_31",
        "dyd_results": "BM",
        "school_grouping": "3",
        "grades": "1,2,3,4,5,6,7,8,9,10,11,12,13,14",
        "ready": "YES",
        "roster_option": "2",
        "assessment_groups": "1",
        "tracking_id": ""
    }

debug = False

def main():
    """
    Main entry point
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("--username", help="mClass user name")
    parser.add_argument("--password", help="mClass password for specified username")
    parser.add_argument("--config", help="Report configuration data")
    parser.add_argument("--out", help="File to write result")
    parser.add_argument("--debug", help="Print debug info",
                        action=argparse.BooleanOptionalAction)
    args = parser.parse_args()
    if not args.username or not args.password or not args.config:
        print("--username, --password, and --config required")
        sys.exit(2)

    global debug
    if args.debug:
        debug = True

    data = get_configs(args.config)
    session = login(args)

    if args.out:
        # Get the report
        dyd_response = get_dydreport(session, data)
        try:
            with open(args.out, 'w+') as outfile:
                outfile.write(dyd_response.text)
            print("File complete!")
        except Exception as e:
            print("Error writing out file: ")
            print(e)
            sys.exit(1)
    else:
        dyd_response = get_dydreport(session, data)
        print(dyd_response.text)


def login(args):
    session = requests.Session()
    # Get redirect to shared login page from Rasberi
    report_redirect = session_request(session, "GET", CONFIG["mclass_baseurl"] + CONFIG["reports_path"])
    # Get shared login url to POST credentials
    login_selector = Selector(text=str(report_redirect.content))
    kc_url = login_selector.css("#kc-form-login").attrib['action']
    session.headers.update({"Content-Type": "application/x-www-form-urlencoded"})
    auth_data = "username=" + args.username + "&password=" + args.password
    # POST credentials on shared login page
    # Shared login page will redirect to /reports/kc_callback that will setup user session
    # and redirect user to /reports/myReports page.
    response = session_request(session, "POST", kc_url, data=auth_data)

    if 'rasberi_sessionid' in response.cookies and CONFIG["reports_path"] in response.url:
        return session
    elif CONFIG["reports_path"] not in response.url:
        raise ValueError(f'Login page redirected user out of Admin Reports.'
                         f'User {args.username} has Standard user access rather then Full or System.')
    else:
        raise ValueError(f'No cookies in login page response. Incorrect username or password. '
                         f'Used auth_data="{auth_data}"')


def get_dydreport(session, data):
    """
    Make request for DYD with config data
    """
    if debug:
        print("Config data: ")
        print(data)

    data = "data=" + urllib.parse.quote(json.dumps(data))

    response = session_request(
        session, "POST",
        url=CONFIG["mclass_baseurl"] + CONFIG["dyd_api_path"],
        data=data)

    if response.status_code == 500:
        error_page = Selector(text=str(response.content))
        exception_tag = error_page.css('.exception-id *::text') if error_page is not None else None
        exception_str = exception_tag.get() if exception_tag is not None else None
        print(exception_str)

    return response


def session_request(session, method, url, **kwargs):
    """
    Make a request on the session,
    printing debug info (including redirects),
    and exiting on errors'
    """
    try:
        response = session.request(method, url, **kwargs)
        if debug:
            if response.history:
                for resp in response.history:
                    print(resp.status_code, resp.url)
                    print("Request method", resp.request.method,
                          "Request headers: ", resp.request.headers)
                    print("Body: ", resp.request.body)
                print(response.status_code, response.url)
                print("Request method", response.request.method,
                      "Request headers: ", response.request.headers)
                print("Body: ", response.request.body)
            else:
                print(response.status_code, response.url)
                print("Request method", response.request.method,
                      "Request headers: ", response.request.headers)
                print("Body: ", response.request.body)
    except Exception as e:
        print("Error getting session request: ")
        print(e)
        sys.exit(1)

    return response

def get_configs(config):
    try:
        with open(config, 'r') as data_in:
            data = yaml.safe_load(data_in)
        data = DEFAULT_DATA | data
        return data
    except Exception as e:
        print("Error loading config file: ")
        print(e)
        sys.exit(1)

if __name__ == "__main__":
    main()