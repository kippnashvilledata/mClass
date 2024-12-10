"""
Script to download DYD reports
"""

import sys
import json
import urllib
import argparse
import requests
import yaml
from parsel import Selector

CONFIG = {
    "mclass_baseurl": "https://mclass.amplify.com",
    "portal_path": "/portal/",
    "myreports_path": "/reports/myReports",
    "dyd_cannedreports_path": "/reports/CannedReports",
    "dyd_cannedreports_api_path": "/reports/api/report/CannedReports",
    "dyd_path": "/reports/DownloadYourData",
    "dyd_params_path": "/reports/api/parameters/downloadyourdata",
    "dyd_export_tracking_path": "/reports/tracking/export_tracking_id",
    "dyd_api_path": "/reports/api/report/downloadyourdata",
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
    parser.add_argument("--username", help="Your mClass user name")
    parser.add_argument("--password", help="Your mClass password")
    parser.add_argument("--config", help="Report configuration data")
    parser.add_argument("--out", help="File to write result")
    parser.add_argument("--debug", help="Print debug info",
                    action="store_true")
    args = parser.parse_args()
    if not args.username or not args.password or not args.config:
        print("--username, --password, and --config required")
        sys.exit(2)

    global debug
    if args.debug:
        debug = True

    try:
        with open(args.config, 'r') as data_in:
            data = yaml.safe_load(data_in)
        data = DEFAULT_DATA | data
    except Exception as e:
        print("Error loading config file: ")
        print(e)
        sys.exit(1)
    print(f"u={username},p={password},c={config},o={out}")

    session = requests.Session()

    # Login
    portal_redirect = session_request(
        session, "GET",  CONFIG["mclass_baseurl"] + CONFIG["myreports_path"])
    login_selector = Selector(text=str(portal_redirect.content))
    kc_url = login_selector.css("#kc-form-login").attrib['action']
    session.headers.update({"Content-Type":
                            "application/x-www-form-urlencoded"})
    auth_data = "username=" + args.username + "&password=" + args.password
    portal_response = session_request(session, "POST",  kc_url, data=auth_data)

    # Get the report
    dyd_response = get_dydreport(session, data)
    if args.out:
        try:
            with open(args.out, 'w+') as outfile:
                outfile.write(dyd_response.text)
            print("File complete!")
        except Exception as e:
            print("Error writing out file: ")
            print(e)
            sys.exit(1)

    else:
        print(dyd_response.text)


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
        print(e)
        sys.exit(1)

    return response


if __name__ == "__main__":
    main()
