import logging

import requests
import time

max_attempts = 5


def make_get_request(url, params=None, headers=None, timeout=5, allow_redirects=True, verify=True):
    """Thực hiện yêu cầu GET."""
    attempt = 1
    while attempt <= max_attempts:
        try:
            response = requests.get(url, params=params, headers=headers, timeout=timeout,
                                    allow_redirects=allow_redirects, verify=verify)
            response.raise_for_status()
            print(f"[GET]- Request: {attempt}")
            return response.json() if 'application/json' in response.headers.get('Content-Type', '') else response.text
        except requests.RequestException as e:
            # logging.error(f" GET request error for {url} on attempt {attempt}: {e}")
            if attempt == max_attempts:
                print(f"Gọi API thất bại quá số lần cho phép: {attempt}")
                return None  # Trả về None sau tất cả các lần thử
            attempt += 1
            time.sleep(2)  # Chờ 5 giây trước khi thử lại


def make_post_request(url, data=None, json=None, headers=None, timeout=10, verify=True):
    """Thực hiện yêu cầu POST."""
    try:
        response = requests.post(url, data=data, json=json, headers=headers, timeout=timeout, verify=verify)
        response.raise_for_status()
        return response.json() if response.headers.get('Content-Type') == 'application/json' else response.text
    except requests.RequestException as e:
        logging.error(f"POST request error for {url}: {e}")
        return None
