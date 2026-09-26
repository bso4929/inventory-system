import streamlit as st

# -----------------------------------------------------------------------------
# 위험/삭제/취소 계열 버튼 색상만 기존 앱의 초록색으로 통일
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* 삭제/취소 계열 버튼만 초록색으로 변경 - 다른 버튼에는 적용하지 않음 */
    [class*="st-key-modal_cancel_add_user"] button,
    [class*="st-key-modal_delete_order_items"] button,
    [class*="st-key-modal_confirm_delete_"] button,
    [class*="st-key-modal_cancel_delete_"] button,
    [class*="st-key-modal_delete_user_"] button,
    [class*="st-key-modal_cancel_edit_user_"] button,
    [class*="st-key-bulk_delete_row_"] button,
    [class*="st-key-bulk_item_cancel_"] button,
    [class*="st-key-bulk_item_save_"] button,
    [class*="st-key-modal_cancel_quarter"] button,
    [class*="st-key-modal_delete_quarter_"] button,
    [class*="st-key-delete_inventory_modal_"] button,
    [class*="st-key-cancel_inventory_modal_"] button,
    [class*="st-key-confirm_edit_item_delete_"] button,
    [class*="st-key-cancel_edit_item_delete_"] button,
    [class*="st-key-delete_from_edit_item_"] button,
    [class*="st-key-cancel_disposal_confirmation"] button,
    [class*="st-key-confirm_disposals"] button,
    [class*="st-key-delete_disposals"] button {
        background: #2e8b57 !important;
        background-color: #2e8b57 !important;
        border-color: #2e8b57 !important;
        color: #ffffff !important;
    }

    [class*="st-key-modal_cancel_add_user"] button:hover,
    [class*="st-key-modal_delete_order_items"] button:hover,
    [class*="st-key-modal_confirm_delete_"] button:hover,
    [class*="st-key-modal_cancel_delete_"] button:hover,
    [class*="st-key-modal_delete_user_"] button:hover,
    [class*="st-key-modal_cancel_edit_user_"] button:hover,
    [class*="st-key-bulk_delete_row_"] button:hover,
    [class*="st-key-bulk_item_cancel_"] button:hover,
    [class*="st-key-bulk_item_save_"] button:hover,
    [class*="st-key-modal_cancel_quarter"] button:hover,
    [class*="st-key-modal_delete_quarter_"] button:hover,
    [class*="st-key-delete_inventory_modal_"] button:hover,
    [class*="st-key-cancel_inventory_modal_"] button:hover,
    [class*="st-key-confirm_edit_item_delete_"] button:hover,
    [class*="st-key-cancel_edit_item_delete_"] button:hover,
    [class*="st-key-delete_from_edit_item_"] button:hover,
    [class*="st-key-cancel_disposal_confirmation"] button:hover,
    [class*="st-key-confirm_disposals"] button:hover,
    [class*="st-key-delete_disposals"] button:hover {
        background: #26734a !important;
        background-color: #26734a !important;
        border-color: #26734a !important;
        color: #ffffff !important;
    }

    /* 버튼 내부 텍스트도 기존 초록 버튼과 동일하게 흰색 유지 */
    [class*="st-key-modal_cancel_add_user"] button p,
    [class*="st-key-modal_delete_order_items"] button p,
    [class*="st-key-modal_confirm_delete_"] button p,
    [class*="st-key-modal_cancel_delete_"] button p,
    [class*="st-key-modal_delete_user_"] button p,
    [class*="st-key-modal_cancel_edit_user_"] button p,
    [class*="st-key-bulk_delete_row_"] button p,
    [class*="st-key-bulk_item_cancel_"] button p,
    [class*="st-key-bulk_item_save_"] button p,
    [class*="st-key-modal_cancel_quarter"] button p,
    [class*="st-key-modal_delete_quarter_"] button p,
    [class*="st-key-delete_inventory_modal_"] button p,
    [class*="st-key-cancel_inventory_modal_"] button p,
    [class*="st-key-confirm_edit_item_delete_"] button p,
    [class*="st-key-cancel_edit_item_delete_"] button p,
    [class*="st-key-delete_from_edit_item_"] button p,
    [class*="st-key-cancel_disposal_confirmation"] button p,
    [class*="st-key-confirm_disposals"] button p,
    [class*="st-key-delete_disposals"] button p {
        color: #ffffff !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

from supabase import create_client, ClientOptions
from PIL import Image
import io
import base64
import html
import uuid
import re
import time
import httpx
from contextlib import contextmanager
from datetime import date


# 사용자 화면의 취합/폐기 저장 버튼만 기존 앱 초록색으로 통일
st.markdown(
    """
    <style>
    [class*="st-key-save_collection_requests"] button,
    [class*="st-key-save_disposals"] button {
        background: #2e8b57 !important;
        background-color: #2e8b57 !important;
        border-color: #2e8b57 !important;
        color: #ffffff !important;
    }

    [class*="st-key-save_collection_requests"] button:hover,
    [class*="st-key-save_disposals"] button:hover {
        background: #26734a !important;
        background-color: #26734a !important;
        border-color: #26734a !important;
        color: #ffffff !important;
    }

    [class*="st-key-save_collection_requests"] button p,
    [class*="st-key-save_collection_requests"] button span,
    [class*="st-key-save_disposals"] button p,
    [class*="st-key-save_disposals"] button span {
        color: #ffffff !important;
        font-weight: 700 !important;
    }

    /* 배분 요청 목록 하단 원가 총합계 텍스트 */
    [class*="st-key-request_panel_distribution"] .save-collection-total-cost {
        font-size: 22px !important;
        margin-top: -4px !important;
        font-weight: 700 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.set_page_config(
    page_title="Beauty Consultant M/UP",
    layout="wide"
)


# -----------------------------------------------------------------------------
# 버튼 UI 공통 스타일 정렬 패치
# - 모든 Streamlit 버튼 텍스트를 동일한 Bold 두께로 통일
# - 기존 개별 버튼의 색상/크기/기능은 건드리지 않음
# - 가로 버튼 행에서는 버튼 자체의 세로 정렬만 일관되게 유지
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    /* 모든 Streamlit 버튼 텍스트 Bold 통일 */
    [data-testid="stButton"] button,
    [data-testid="stButton"] button p,
    [data-testid="stButton"] button span,
    [data-testid="stButton"] button div {
        font-weight: 700 !important;
    }

    /* 가로로 배치된 버튼들의 버튼 영역 자체 정렬만 통일
       (입력창/텍스트/데이터 영역에는 적용하지 않음) */
    div[data-testid="stHorizontalBlock"] [data-testid="column"] [data-testid="stButton"] {
        display: flex !important;
        align-items: flex-end !important;
    }

    div[data-testid="stHorizontalBlock"] [data-testid="column"] [data-testid="stButton"] > button {
        align-self: flex-end !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)

LOGO_DATA = "iVBORw0KGgoAAAANSUhEUgAAAvoAAACECAQAAABLoUfGAAAhnElEQVR42u1de6COVfZ+Dsf9WslUcsmtixGiSAkppRulC8W4pUwSamr4paEkSmSQdBFRUZguJNVULjVpJCSl0EhEScj9+v3+OB3O4Xzvevbte8+ZWfv583xn7bX3u9/n3XvtZ6+NBBQKhULxvwLtAoVCoVDSVygUCoWSvkKhUCiU9BUKhUKhpK9QKBQKJX2FQqFQKOkrFAqFQklfoVAoFEr6CoVCoVDSVygUCoWSvkKhUCiU9BUKhUJJX6FQKBRK+gqFQqFQ0lcoFAqFkr5CoVAolPQVCoVCoaSvUCgUCiV9hUKhUCjpKxQKhUJJX6FQKBRK+gqFQqFQ0lcoFAolfYVCoVAo6R/5sVtJRyU0ws3og0EYgZGYgHEYjgHogatRFenQokVLslIQddARD+MFfIBvsRVbcRAJJLATP2IFZmME/owG+hblsZIfVXAV7sFwvIAZmPM7ZuFFDEdvtEQ1pHGGchvpn4x2GItF2BtpfB8W4BFcgkI6ErQEKOkoLaKog/2ihP3SVqP7HPwNc7CLekW3YybuxIn/E3TJ9LdNKR7gGR5d0nAe+uBd4qluxdvohWp5h/Qrog8WGa49tmAsGnocHIMPfz+T4bFAw7K7WPPkyP+vL/7/aGcf64h1PBv5/4+K/2+LoZ6fxsm/z4yjsNTaegn8QIztPfLLm61UwiCstli/78cbaMHOESNKPeI51bf4/H4oWr1dtNKM6omzLFq9VLDZybFXq+Eh/Mf4mX6K21Akt5P+5ZiFQ9Zhp4Vo5WHQAsAysa6xgUj/NbHmD4VXXvr/Dc4+viLWET3ElwcLPD7r/XnMJGo9w9L2CKpN9xpYbIDXHN6fBBJY7PwOdSZqOdvYahXCanfRSjeqDx61aPVOwWYjhx69ELMcnuhP+AsK5lbSvwyLPbz2n6OBh2XUbrGeewKR/jJnYtsiWijl5GEVcfa7NtkgAwDkE0J2LrjX+/O4jqj1ASvLdYlVRAKf0RH3MzHDUy9+iOoOPfYQUUNxY6uXE1YvFa0Mo9q/DvkMvTtJtHmS9Qx/pocnugoX5z7Sr4K3vb34hzAaJZxe9PJELS2DUD7zuZGI7UPRwnlOPj4l2u8mhO/CSQyu9f5ECmCTWOsyq+jyQirkUpOyVhhDsN9jP+5BX2PiyywvitZ/sbDag/C6imjlDbL9zQy9ayTumtjtKD3gbYJ0CEORP/eQfhruJDeceKy0WEAeKU2JGmoEIf1yHojtCdFCewcPy4qfpeh5PhtXtUPNAM9keJAAz11UewZQtmrjqwB9OdtyS/MjYvViXv5OfCDlNREbWHzB0LsOYtDMvFTAAs9P9N2j1/hxkX4pvB7k9d+OK6xf867EdzOMXqixB2LrIFoY6ODhINF6Dy9xVTsUDfBM/hggwHMqfiOsfkmNsj8Rq0M7fI1TLfprvWh3qoXVGcRETyp8YHEHihl5N9B7iy8kVpjm+DQ77cdD+pWwIhgB7MP1lq/5UNH294Ei+l2IdhURbNQSLUyz9q+4uGOwQfRvWLAnvj7QU5EDMcsNLf6DaM1BIgyXJtKNayzYlPYLEVZtlG8yT8wSbZgEFtsZefeSYG2QYWuvCbbv9UnW9zMO0q+JjUGH7D5cHkhB834gehki1vwDEYXeJ9j4wtq/e0T/enmLq5pjbqCn0s3D+iv7K8205nGC8p8K+v5kfM5KGvXV6YTNOyx2QPaJVkeJVi42CoX4nBaYCTZvwoGAT/SVI+qs1JN+jSALmOzYhtODKGhCCTanOwo2M8rn4jad3SZdQawTLP8szvNDCjbHBXoqpYkACh8yK4611K6UHKoalZLz9zOMJJyMysY88HoaYbWnh7Bt1nXWKQb+bRasNTbqwX2Bn+idcZF+eZFA/GCpcfQ9TsHmUrFmRon+vGjlNCvvOol2+3iMq5qjD0IVWZGywuvGcAJNRDv3pyztSk+DnrojyLb3pYTVKz2Ebe3kv8eJtsrRtmpQuz2u2qwz4yD9YliSsiFrGk9jBJtXByKXnV6GoqwMaWHhW5qoEfmF0F+HFGy2Dkb6jOKIC/CcQy3dnxLtXJey9yeBXahE99RjhL3CQQJs8tmC14xazQtx6wqWdtKWSlmdpTbHnIzVW2pJf7Khk5swD9MwARMwHZ8ZCjz3GR41aRxkrsIUH4JNALjIQ+TdJhLdxxN92qJWMNLPRxyBZwI8nDp/rRhHr4btRj3zM97EY+iFLuiMezAM72Cr0f//g+6paaKtjRb9L2/+HxSEwlzYNjtqk961EaMNbJlq4N1XGI12aILaqI3zcQuGG7XvxlSTfmeDf1+EO1H5qP9Px/kYgW20jSmeFTTMALMpjT3NJ0t5mEkeWz4WbG6lTvqGFGwWQ7jyNy8BHk6dL8W8C4i7Nlmly2NQN4c9nAK4Am8Z9G0dsp8+Ey39y6L35c3//3gJ22bHMNI7KdA2nbRzi8FmbM7Krlr0dHol0lNJ+hXoqNXiyMhmaYymT6OZpKwa4mGA2RUfgs2M8p2H7eDs5UJPB4nkOdsaKhPisSiFkKUikdOmrmCDU+dPFH0ZQI/7p1FG0LP84HnitFm09LJF78ub/+95CdsevSbJT3k3XrAzhLJShui7jMlFdLq6hmSIqH0qSf8tcsD2J7r8enKne4RXBc17gYjFh2Azo0g68B+NfZspzvO585vynO195M7ynuj5EMenkkE0J4ihHW4rfDMlWC5LBgUO4GTCWknC0iMWwbW9HtauTS3Wjtze11zBShfKynOUR1OJfbPSoke/nxJOFem3JOPwrcgBcT0Z0yzgUUHzZCBa8SPY5IIRZurrGqK9h73N2cbmUtJvK3q+2nFPJIEEbhD9mE3ZWYeqZLvK4nvKYm/CVi3Czq3GPc/M0WU9XVcL0udWJdIZ5MZUzzHZUZ8h1x5FMY+w1ig1pJ+ObymNrEk6My5BbXOPCpregWhF/tw8R1q62jkUkb1MFI+tl/E2Z7snl5J+YSJ/afJeLUap8+UN00vIWX5Vg5Y1oWwysfhWhJ1LjHuemaPLjDHUgvR3EZOjIl4Em0zCydcMTkycSATunk8N6XNfW7MEuSXwi8cAD6OgiU+wySrR5bmRyTHzCmIQbQhpqaKX1zeu8qRDgOdxouW/Egl4F1CTJtMskVMpqyeIdnoTdqoa9zvDGnICxNcsSJ85S1vTg2CzASUhNRMqyDq5hakg/XzUPP9t40HxAGGVTT2QuwWbvBJd2hR6yMCz4Z7m+Zxgs0auJf261gGe2pQ6v6OnObn5JSD1KLtyyHVkEOUbM0eXBQ7LrEhfDqhKqxtGsCnvdO2nBaTMHtIKDETN1MT0WxM//w0VjBtXkZqncFHs3C3Y5JXo7wuWXqUtHY8d3rbJbyM28HPzfcdfiP7XzzGo9W/i2b5D1M/coLTS4vATqOmY/DGRc2GutfBNnqPLAoc0y1ykh0Q+kvJRyYLNCsR1Og9b9Fu1HPYJfqf7jJIK0meGfv9A0fAELqIs5W7BJr/AG+Zh/pFR+gmWdlO6DnbO9j1yc+lppe2+k9LTy5OdmtQLZ5dblplNzxatfCnamBfk7Zbn4+WtKD+BBP5PsDzGOfQppyvfYHHX2NEriGx0nyrSP4f48S+WjWMiprdTlnKzYNMkdXB7kaq5pGtFxLR4JnLY+PKX+illxI3otcdstp1CqfO7E7WPJOwssrzhtgV1UlgqO0QbEy18k/e65IxUTa1J/2vBsiTllQSbBfGz6EM3y/F6dTK6TxXpMyqbAZaN+5O3SGduFmyapA6Wr/6oRNnpLopryxl4FV/+Ul9FTjPQwPg/EphPUHVBSrDQxrJd5alQR3Rgs2yQN5zZ65IFDvJmcPIQS/S9BtJBSEmweSNxdqOw5VMthAFRZ/hDkz5z1+g+/MGyccwqgjtTmJsFmyapg9OxR7B2GWXlO48kHWf+Ul+lhWGA5ypiZO6hTowzcsh19DXqxxYmG0/lSAvnedmsttnrkgUOUvhqf4SCKSpTfwFxi16aFE0RW9cv1GAOTfrMoayp1t4zcwwmLMPMKq4M9AT8CTYzipQFhUmY21b8TJtsu8d34by/kl88ipM1wFOMOvjESZSZ87yDHFrG3LN7TqSFNoSFJkH2umSBgxRY/AZXJv3bpoijnVUdBZtFxJDYAYM9s1xG+uOJn7ay9j6dsP6Jp1lFtSD971ewCcjHuscQNhYLNp428ii+C+d9FnnbraHRXtNn1Oy8MJVb9kyHdn3kTNl9CQsVAvR3gtgJlAKLM1AgIrZ+TVK70qUxkmBCVjTODDeUw5J+PuJixG1OUkh5s4zJjy3PKg4YJHTwvYg1Sx0saUY+EC00F/vC7KBNfBfO+yzVxFZkhgMYdf5+Mg8/s9G61KldM4garom08AzR2vzGfskHx+RkzXJgcRgQkcBxqvVbJgk25ayYbfIq6Z8bNLjDRSTXEFZkBc3qQP3vV7AJyHkx14kWJK3/BMM25nXBZmaR8pr8iHxg1fnsxubowMEd4HWihpsjLcgp6b6z8GuxaHW+h8Di7QDqJ/3r3qTpBJ9wEmymiTud+0Jmjw1L+kwy2A6BSX8dYUVW0MwO1P9+BZsAUEJM4RS9KD7X8zw/7ws2M0tHOZUVOHX+l/TKZg1h7fzgpB+9DbsqyPOVr4sZ7yGw2BQAsDLp329LYvlNJ8GmrLF7J+RADkv6HxI/LBeY9JmZ/lJ66e67+BVsQhjCzLactKw2z4suCzYno5IF0lNM+sVEIhpFqfMPCmLAI6UC8f5sswidmJJ++4j/z0ekOX/O2KuTCK8e8BBYzGCf/kn//nESy1LW2GjBZi/Rr155lfTTCWXKKkf/94g1MCdpZT97Bup/+c7gccY2pzos1qsJ64RDOMvQG9uD8DLKINXlOTHAw2hthtH1tSWsua5BmZTNrRw/TObiwwu8nE2Q1tE7fv9dVUO5app4WK+c44e2dl4lfSad0/NO3hclalgiWolTsCkvYvsY25SucXsw4n+f9nLqwSyuaocdMQR4GnrweyWK0vWN8nJAKbosdCT9i4j/b2fsVQfCqpwmXFpHLz78y0+MEsRIY1oSbP4q/P+v5Ln5XEj6zM2g3Zy8P9UL6ccn2GQWsa2NrV4pWHwlwh9p5WQurWwaiPS/jCWuv8LZ76YGtS0i7F3s2CLmkr1LnXY6sopZ2TKQsCpvdS6l34TuEbGIY09NS1lPo/VUlcWWzQo7iEOS/kTiZ+c6eX82UYOclCk+wWYj74JNZuWS/DM4WPjP1y3a2DUQ6c+MhfTvc/Ta5CRzQSoxs6vKgzmRG7VVzIg1TjH2Sj6vutlD2Hbg4V+WwX6DT5bEGNGCTfnWPykB+olo4oAzQpL+54R+102ffTnhyCvOkb9wgs1O3gWbGSVaELYrScaXkiIB1LHwZWgg0h8VC+mfRBFx8lO7JtdVMlOalY7tKUz5HaXXkqd2ey2SwclrnAUewrZZN6hnGHyopcnR0Ei/5GNn1wgt6+H05owMR/r5iLOEyx2H7G2EI3KiNPkYSCjBpvz411vZfVewWjHH/7o3wDzf9uYiGXcjnvKmg89mO0NMeoPXHFtzOuV3lMhXvpX1Gwu/5CsqJ3kI22ZVUd2U9FdbjpmaSozRNdIv+YpE6fzy353enEHhSL8a8aOpjkP2ES/KgcWxzSrlz81cK7uPCVab5xhM+FH4r/pWviwLRPrXxUT611p7PMmwpoeDH8yST18nkMCeSAvrAkyZTvByvE0O2x6X5ddFsI3eV5NiGNH7NhtEiYK0Mprl9Ob0Ckf6THbAhxyH7EtetoplBU0owab8uRlnZfdmwepdFq+I3WonnGDznJhIvwB+svL3J+Ku2eyFUdDfkoK18trIfYdD4v+bp81m7o5t7xy23XTU78fTa9xtguXyEV6VElu20Mvme4TUNRzp9yR+1M5xyP6LqEO6zpxR0FweiEBCCDYB4CzB6uhj/iOfqEtpYOVJKMFmAscjrjLMyt8bjOv5grB6nmNbmLVyVMrC6sT/32fsVXvCqjweJcHmR0f9vlnE3mOZbNuo0XZ3R87U5RuXXxSnHQec3pym4Uj/UeJHFzkO2S1EHdJ15oyCpkqgTcEQgk0AyC/Mr983DlrY3hsWSrD5G+IrNSz8tYm9M5enlHVsC3OYbJJjeOhGY68eJKzK6yZJsDn+mIlP8vTZ3Q3WIdEpHuXLU6R7cas5vjsB1TuTiR9VcBqwfyBqkK8zlxU0+wMd+A8j2Mwo/zZcsH8i+NHE0o9Qgs0vEGdZYOjtFpxkXAejq9nt3BImm37U/dW3B1mNvEgkn5CLJNjsa7AX9mmWX7Vz+sD3Ftt2q9CuKx3fnVLhSH8uoX53yxrShHBDzt8oK2hWBqKOUIJNQD5Zm92udKpyjnUbQwk2X4+V9G839LajRR1VCLsrnPcn9jsGYYcQ/39igI/qItFGOYtVdK2IX59++Ff9nQSbj4l+XSK0rKfTm7M95OGsb8WfrHMcsncTbsj5/WQFzVuBqCOUYBMA/mykuJ8VaJ7PCDb3YYkF+sRK+iWpq00y8a5VHUx6A1cp8dmU/1HR81eDpMvYLFqV04HIgs2aRvsoR3RSk5wEm8+LflUXWjbKifS/Dkn6crz9c8chO4lw43HRiqyg+Xsg6ggl2ASA8wXLbbP8tqbzMZjkZVnwURBPmUS/CDssg5iM+u1lx1Z0Juo4hBLWYUS7dBnHEV4NFK10EduV07XjyU9crzm8Pfuxk2BTngZJEoXZTqT/XkjSlxOu/tNxyC4n3JAz8ckKmh6BiCOUYBMAiglSugEGEVQX7dLO4MQVT+E3qLtb1sDktBnt2ArmipavHDebzdNlMFcvdRKtSIGnnAO/p0a8N5nr3Z8dBJvAHLFtkkrfTbA5PiTpyz951WnAHk8ohOVEablbsHm/g/VvIi1PPvy7CoIAzGWez+Qv7Z8nST8N31GvwXzrfIndCesPOrbiM6KOiRH/X5w59G/sFZNQupFoZbo8482xfChMwUo4CTZl0t8i7sO4CTYHxkv6E5wG7NVEDb+KX83cLdi8wcH+K5GWjySVHSn4cJWDD42JNrZF3izvUGdZq1vb70XYd7tqozgOEnXc5bgnYJ4u4wHCqqyGWmq5SuocoRgqAqCOk2BTJn3pasmKWCNgR6T9LnmZ9B8napBTlOZuwWYdB/t9Iy3v/P1zWEYYIostkmXxcVXXNsZZmEX2fQ72w5P+5dSLHCW4vCZIugw5hRuzOSwFFpOdsi8VccalDYDWjicyJNJf4jwyo89eXJyXSX+5l5cidws2SwR8pTO2FyX5WSunNjKCvmJ5kvKZRfYSp+nCbcFJnzlZvCVSVs2IB83TZci3yS31EFhskfR/X42cRP7VSbCZCtJfG2m/UkjS3x6U9CtRTshX++VmwebGoOGjSwAUFTbiljrN85kbgH/Io/N85lTkYKcaOgYn/W+IGqJTIj7h5eRs9pJOSEDkRI1yYLGyxfrlAP6AZ50Em7J65zvHkXmyHLcIR/rrgxxNN1n8riXs5GbB5nzHGjaKmiQpL3cbRw/kC+ffz6Ok38KLwiSqtCRq6Odgvzr1Gt/qsG+UQAJ7jf36I+HVAOfA4r6IFUyBiHMCvSM2ehnBZlRatwxschyZHeRPSjjSXxyU1JibPZnsfvJ65M5AtCH3z3jHGqL1vKOQjjWCWM/1pk5ZsDk6j5I+c41FI6camPt4XSYkA6jXOFp++LH4/2uM/WK0O7LAQQosRgtRx0TscX3v1GOyZwcc9xCjV9dvhyX9meJP/mPdsLMoFxo7h0ASiL4f1KWEFWzKw+td3BJ4ns8INu/Ko6TPXGNxolMNlYkaplhbT8Mqwv6/nKPv5hHqwYRfcth2mmDhDesP7iEnwSYjxXXJSCadFX80LOmPJH5U0rJpT1JZd+R4NKOgOS0IaYQWbALSzUtrheDLKud5PiPYvCyPkv5bYsu2OdZQgBBULrO2fgn1Et8hWFkT4Ey5fEHIPmIuLK2jhwqfRNsDUPITaRH0nbiVEUiHI/3uwRbAxxFhA24brRMxwPIHIY3Qgk0AOMPpEEdH5zYygs1KeZT0V4ot+8y5Dvn4134xh2yyMpN4NtmzyNuR/hxjzzZ50O7I62gpk+WDlm+NvE9ZKegKfwkzhQ1H+gytPWLVsMGUA6cTlmQFzYpApBFasAkA+aiPY7J5vvvpBFmwudt5NRFPSSeyU77kXAtzc1ZTK8u1qNPsb4h2ZNI33bdjcos+52EdLYV+q1u+N0NF39KwNZi44TJOfh6O9IsTSmYbSi1HXcDHZfyQFTQzAtFGaMFmRvnEmvS7eKh9upc5W24sDDUNcK7lb0Qtdrc3v0ONATn9yOfeA1C3En51Fa3IE075RO+/rd6brkQb3xO3cu1uhcuHRYLlMaFJn1PYXGjctBmeNnGZyF8CTwSijSnBBZsA8JQl5a+1DhtkLbJgc1oeJX3mLOstzrVcTNSy0eJJtaTGwApiT0zO97jDcC3HrG6qOq+jmXvX7rJ6c5iVVz/Ryl+CxPMPZ+oPSfqDiJ/NCTATYK4W5iJ/9jkSpbJIrHm8h1putyT9bl7aKAeXBuZR0mcEm/WcaymKPQGe1QnC+Q2TPZ2xXij6SClLHMxiTt9IzLOI8mW/xZtTnrAsX/u+Lse0z9GlIn4TrK7P/ACHJP3zqR92NmhYQ+ylbF5FDrH4BJvbggs2AaB+jPN8RrDZPo+SPiPYLOWhnllEPT8ZnXlNx7vUGFhN7ekwaRhMRLkPE/bGeAjbvuyt900FmxlhmA3eT3MXJUJtQzJ/HJL004iNngR2oT5NYZupqueR9i6ITbB5YgoEmxlD4aAF6ff00kZGsHluHiV9WbD5s5d6uBuGZ9IKs3xiEoFM3EzZa0BY+gYFSO+qUrt1zTyEbbmU1G2N35zlZEvHiJYOkAHqjFKQCHrvP7IKCUn6wEPUTzfjfKJhrYnZcQIJHERtsqs6xCbYZD43frJPfmU8cDegiJeau6RoNhxHkQWb873UU4pc2T5NRc4L4WVyDHxK5lxKp97JhylbJfAlYesHqqVS2JbbbylKhH9N9U4ZpR5ha1vkNZXZA3ZzCXuTjvxDWNIvR8bFduPPkcPsZOJmyUyMoF+pgUTHD7DEKY6fG3fBZkZ52Zj0e3kixiHE5yVvFkawOd5TXS+QT226eNDxTEK2kDlt4vcjuGsj+xKft48oSw8RPsmCzXqeez8Tw+h+W0jFQLoSH9/mYmKIjJXDGakifWAC/Q8L0TLHeXVtjBJyvmdXohalO36KReiDRTnHz81GT6Rxn6HfmzzN8xnB5vfoZY0qMZJ+FS80x5Va9JNbg9ZJKaISRhvctzTUwL9LSZtvRiYXqE7N8hPYjbKET428rTCbBxNA3ERa/BhXREQbLqDUTgkcdX9ZaNKvSuzHZ42Evox7cRNaoRU6oT8mE7k6s8etzjMYsIuCUf4u58/NfE+kYTps+3ijxqUBP6kJeukbojCCzdbeanvdoFdWoC/qZtmGL4F6uAf/pI5iZeJLI+VIGnWvRQZhP53jDLsKhlMqJf5UQidvE6r8+NFoVDajLefDFwas+Ay6oO5h9X4hVEZLPE6lxs4MoB+fStIHHg368mdHb6PXaVswP5Y5f258hQfKGvn9C4p7I6udQZ/0CTGSPiPYPNtbbWcZ34l6AOuxCmuwxaJfd6KGoX+tjeyvwxT0w63oiI7ojbFGU4Pt1DxfFmzOM2jdMKPWVQywRso+qd1q9V5dn73q8KRf3PH2dh7Pe1fQ2OJ158/N/d5I48dY5vnlgj7pLYizMILNIh7rG5bCadONxt6liRnmfYG9bVcSbI4zaF0dA//2Gh5EeylF/Tbh6IrDkz5wgdUxB1O8baguvyCgL8OcPzc3eKOMt2ivt6K0t1obB33WC2MlfblH13qtrzC+ThE92E01qhirXGywgM4GJW1Ym91cvJz2cLlhv52AH1LQb4uPXb2ngvS5BbEbPjDYwOUVNLa4w/lz4++68EG01wM8ElXnoE/7pVhJXxZs+r4P7OzAwbIcNvuMyg3BfdtisHUvfYKuNWpbX++CzSOlgdGOpw3W5yQpSQ3pc7dp2mOGMeUzChp7XOr8uSnhjTBuiGGeb/KpscGDMVI+I9gc673W1lbH7EzwhNN9yPcH9W0fmtOeyIJNs12LivQ2+DCLfmsXtN82oWZOlaaK9NMwIljTRlkdoQop2Kzi+LnZ6JEuqpE+D/JKUlODDuY40zcwgs3eAeq9LSjtu+/mDA7m20Gj5HWNRGumSUbmkn7aZay6O1i//Zwz5aeO9DOa53/Y7sCfLAdpOMHmfiH6mDrBZoY4bDvVj2W8UtTioKQfp2DzMsK/q4PU3CZQMOA3XOfFv7uNpKH8LP8mIy8kwab5Ja1dSU+bWfZbzyBPdUXyqWcqSR9ojLVeGzbP4ZBOOMHmaufPzXivZPEx4fMQzwQVdmsvTsEmcyNc9UB1N8Q67335qVEezOhyjZVMNPrUdkPPgcXZxq0qTSbDqGjdb9cLN9uaY1rUCe3Ukj5QEk8a646TDYeODlHIkILNd5w/N/d7pQr5RuGdnuf5JwWl/G2Is8i7UwfoFGPmpQxe9bpOvtfDDWlZy2kOF/fktDVa1tgDKbBos109jfB1r9MtcDWwzGMkX4h+pJr0AeAsTHQk/g34q6MSOqRg80nnz00bry+ifAfBCM/U1Cgo6S+KlfTlfIarggeYlnjoxQN4DqcG8C4/7vWiNfrO8lSzFFjsYWHz2gCCzaNLIQykTyYnxyGMk9fBcZB+xnbYo5ZL1flo7yHfe0jB5t3On5u6Xl9DKaffbpzs+cXvFJT0p8RK+itE/94K7kMaWmGBQw/uxJig2YvKY4LTtG41ulm/49I6urkVIf8aQLCZ0zrJpd8OYAIXqouL9DO2GC/G41hCbv/swiz0ikzbZFJqomMwVI6suQJhoajXV7CQUJv/i2LODti7HY3yK/kvz2CCgA4p8qQWhhrmhkngIN5HVzEjp49SEQONvUtgN6bjCodASRHx6dhNcO4Q7fpSlFXAYMOMYwkk8C368XsKcZJ+Zjkel6IXnsV7WIaNWRQ+e7ERSzETT6ArzvEce9Si5b+hpKEWemGGKJA4gCV4GjemeAu8AFpgJFZRhPE1RqFlSj5Hub/kw0UYigVEuGcPPkA/+hqqXET6xw7k0vrwtWgxKiXRAG1xFx7BM5iAyZiACXgSg9AD16Kmlwsw7Us5XIkH8BLmYjW2Hg5gbMW3mIdx6IVmFhu2/wulAOqhM/rjWczGAizBEqzGcnyEmZiIAWiD2ihkYzYY6SsUCoUib0O7QKFQKJT0FQqFQqGkr1AoFAolfYVCoVAo6SsUCoVCSV+hUCgUSvoKhUKhUNJXKBQKhZK+QqFQKJT0FQqFQqGkr1AoFAolfYVCoVDSVygUCoWSvkKhUCiU9BUKhUKhpK9QKBQKJX2FQqFQKOkrFAqFQklfoVAoFEr6CoVCoVDSVygUCoWSvkKhUCiU9BUKhUJJX6FQKBRK+gqFQqH4L8H/Azcc8gMfOXXqAAAAAElFTkSuQmCC"

def show_brand_header(center=False):

    align = "center" if center else "left"

    st.markdown(
        f"""
        <div style="text-align: {align}; margin-bottom: -4px;">
            <img
                src="data:image/png;base64,{LOGO_DATA}"
                style="width: 180px; height: auto; display: inline-block;"
            >
        </div>
        """,
        unsafe_allow_html=True
    )

# -----------------------------------------------------------------------------
# 글로벌 로딩 스타일
# -----------------------------------------------------------------------------
# 로그인/저장 등 loading_guard에서 사용하는 Streamlit 기본 spinner만 사용합니다.
# 무거운 전체 화면 오버레이나 별도 CSS 애니메이션은 사용하지 않습니다.
st.markdown(
    """
    <style>
    /* Streamlit 기본 spinner의 안내 문구만 차콜색으로 통일 */
    [data-testid="stSpinner"] p,
    [data-testid="stSpinner"] span {
        color: #333333 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)


def reset_loading_state():
    """
    앱 내부에서 사용하는 로딩/재실행 상태를 강제로 정리합니다.

    Streamlit의 실제 실행 상태 UI(stStatusWidget)는 스크립트 실행이 끝나면
    프런트엔드에서 자동으로 제거되므로 별도의 영구 DOM 오버레이를 만들지 않습니다.
    """
    for key in (
        "loading",
        "loading_overlay",
        "is_loading",
        "loading_message",
        "rerun_in_progress",
    ):
        st.session_state.pop(key, None)


@contextmanager
def loading_guard(message="Loading 중..."):
    """
    DB/저장 작업용 공통 로딩 안전장치입니다.

    작업 성공/실패/예외 여부와 관계없이 finally에서 내부 로딩 상태를
    반드시 정리합니다. 실제 표시 UI는 Streamlit의 spinner를 사용하여
    별도 영구 오버레이가 남지 않도록 합니다.
    """
    st.session_state["loading"] = True
    st.session_state["loading_overlay"] = True
    st.session_state["is_loading"] = True
    st.session_state["loading_message"] = message

    try:
        with st.spinner(message):
            yield
    finally:
        reset_loading_state()


def safe_rerun():
    """
    모든 일반 rerun의 단일 진입점입니다.

    rerun은 정상적인 제어 흐름 종료가 아니라 Streamlit 실행을 즉시 중단하고
    새 실행을 시작하는 동작이므로, 호출 전/후 어느 경우에도 로딩 상태가 남지 않도록
    try/finally로 감쌉니다. 같은 실행 흐름에서 중복 rerun도 방지합니다.
    """
    if st.session_state.get("rerun_in_progress", False):
        return

    st.session_state["rerun_in_progress"] = True

    try:
        reset_loading_state()
        st.rerun()
    finally:
        # st.rerun()은 현재 실행을 중단시키지만, 예외/비정상 흐름에서도
        # 다음 실행에 stale flag가 전달되지 않도록 항상 정리합니다.
        reset_loading_state()

def reset_menu_transition_state():
    """메뉴 전환 시 현재 화면의 임시 위젯/다이얼로그 상태를 제거합니다."""

    persistent_keys = {
        "login_mode",
        "logged_in",
        "admin_login",
        "admin_user",
        "auth_access_token",
        "auth_refresh_token",
        "admin_menu",
        "previous_admin_menu",
        "user_menu",
        "user_collection_mode",
        "show_user_collection",
        "collection_user_id",
        "collection_identified_name",
    }

    for state_key in list(st.session_state.keys()):
        if state_key not in persistent_keys:
            st.session_state.pop(state_key, None)


if "login_mode" not in st.session_state:
    st.session_state.login_mode = None

if "logged_in" not in st.session_state:
    st.session_state.logged_in = False

if "admin_login" not in st.session_state:
    st.session_state.admin_login = False

if (
    st.session_state.login_mode is None
    or (
        st.session_state.login_mode == "admin"
        and not st.session_state.logged_in
    )
):
    show_brand_header(center=True)

    st.markdown(
        """
        <h1 style="text-align: center; margin-top: 0; margin-bottom: 1rem;">
            Beauty Consultant M/UP
        </h1>
        """,
        unsafe_allow_html=True
    )
else:
    show_brand_header(center=False)
    st.markdown(
        """
        <h1 style="margin-top: 0; margin-bottom: 1rem;">
            Beauty Consultant M/UP
        </h1>
        """,
        unsafe_allow_html=True
    )


url = st.secrets["SUPABASE_URL"]
key = st.secrets["SUPABASE_KEY"]
service_key = st.secrets["SUPABASE_SERVICE_ROLE_KEY"]


@st.cache_resource
def get_supabase_clients():

    supabase = create_client(
        url,
        key
    )

    admin_supabase = create_client(
        url,
        service_key,
        options=ClientOptions(
            auto_refresh_token=False,
            persist_session=False
        )
    )

    return supabase, admin_supabase

supabase, admin_supabase = get_supabase_clients()

@st.cache_data(ttl=300)
def get_active_categories():
    result = (
        supabase
        .table("categories")
        .select(
            "id, category_name, parent_id"
        )
        .eq(
            "is_active",
            True
        )
        .order(
            "category_name"
        )
        .execute()
    )

    return result.data


@st.cache_data(ttl=30)
def get_current_quarter():
    result = (
        admin_supabase
        .table("quarters")
        .select(
            "id, year, quarter, start_date, end_date, status"
        )
        .eq(
            "status",
            "collecting"
        )
        .order(
            "year",
            desc=True
        )
        .order(
            "quarter",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if result.data:
        return result.data[0]

    return None


@st.cache_data(ttl=10, show_spinner=False)
def get_all_quarters():
    result = (
        admin_supabase
        .table("quarters")
        .select("id, year, quarter")
        .order("year", desc=True)
        .order("quarter", desc=True)
        .execute()
    )
    return result.data


def resolve_new_hire_target_quarter_id(
    distribution_title,
    fallback_quarter_id=None
):
    """신규입사 배분의 저장 기준 quarter_id를 결정합니다.

    핵심 규칙은 '현재 메인 취합 분기'와 신규입사 배분의 분기 기준을
    완전히 분리하는 것입니다.

    - 사용자가 2026년 3분기처럼 연도+분기를 직접 입력하면
      그 값만 기준으로 사용합니다.
    - 해당 분기가 아직 quarters 테이블에 없더라도 현재 분기로 대체하거나
      저장을 막지 않습니다. 배분 기록을 독립된 분기로 남길 수 있도록
      해당 연도/분기의 reference quarter를 자동 생성합니다.
    - 연도+분기가 없는 신규입사 차수(예: 신규입사(5기))만
      기존 호출자가 전달한 fallback_quarter_id를 사용합니다.
    - 연도 없이 3분기처럼 모호하게 입력한 경우에는 현재 분기로 조용히
      끌고 가지 않고 None을 반환합니다.
    """

    text = str(distribution_title or "").strip()

    year_quarter_match = re.search(
        r"(20\d{2})\s*년?\s*([1-4])\s*분기",
        text
    )

    if year_quarter_match:
        target_year = int(year_quarter_match.group(1))
        target_quarter = int(year_quarter_match.group(2))

        # 이미 등록된 동일 연도/분기가 있으면 그 ID를 그대로 사용합니다.
        for quarter_row in get_all_quarters() or []:
            try:
                row_year = int(quarter_row.get("year"))
                row_quarter = int(quarter_row.get("quarter"))
            except (TypeError, ValueError):
                continue

            if (
                row_year == target_year
                and row_quarter == target_quarter
            ):
                return quarter_row.get("id")

        # 과거/현재/미래 여부와 관계없이 수기 입력 분기를 독립적으로
        # 사용할 수 있게 reference quarter를 자동 생성합니다.
        # 취합용 활성 분기로 만들지 않기 위해 status는 closed로 둡니다.
        month_ranges = {
            1: (1, 3, 31),
            2: (4, 6, 30),
            3: (7, 9, 30),
            4: (10, 12, 31),
        }
        start_month, end_month, end_day = month_ranges[target_quarter]

        try:
            insert_result = (
                admin_supabase
                .table("quarters")
                .insert({
                    "year": target_year,
                    "quarter": target_quarter,
                    # 수기 입력으로 자동 생성되는 reference quarter는
                    # 실제 취합용 일정이 아니므로, 분기의 시작월 1일을
                    # 시작일과 마감일에 동일하게 사용하고 즉시 closed로 생성합니다.
                    "start_date": f"{target_year:04d}-{start_month:02d}-01",
                    "end_date": f"{target_year:04d}-{start_month:02d}-01",
                    "status": "closed"
                })
                .execute()
            )

            if insert_result.data:
                get_all_quarters.clear()
                return insert_result.data[0].get("id")

        except Exception:
            # 동시 실행 등으로 이미 생성된 경우 재조회해서 사용합니다.
            pass

        refreshed_quarters = (
            admin_supabase
            .table("quarters")
            .select("id, year, quarter")
            .eq("year", target_year)
            .eq("quarter", target_quarter)
            .limit(1)
            .execute()
        )

        if refreshed_quarters.data:
            get_all_quarters.clear()
            return refreshed_quarters.data[0].get("id")

        # 여기까지 왔는데도 ID를 확보하지 못하면 현재 분기로 대체하지 않습니다.
        return None

    # 연도 없이 분기만 적은 값은 현재 메인 분기로 대체하지 않습니다.
    compact_text = re.sub(r"\s+", "", text)
    if re.search(
        r"(?<!\d)[1-4]분기",
        compact_text
    ):
        return None

    return fallback_quarter_id


def parse_quarter_hierarchy_label(label):
    """자유입력 명칭을 계층형 분류로 변환합니다.

    규칙:
    1. YYYY년 Q분기 형식이 있으면 항상 연도-분기로 분류합니다.
       예: 2026년 4분기 / 신규입사(2026년 4분기) -> 2026년 > 4분기
    2. 그 외에 신규입사 또는 N기가 있으면 신규입사로 분류합니다.
       예: 신규입사(5기) -> 신규입사 > 5기
    3. 분류할 수 없으면 원문을 신규입사 세부명칭으로 보지 않고 기타로 둡니다.
    """

    text = str(label or "").strip()

    year_quarter_match = re.search(
        r"(20\d{2})\s*년?\s*([1-4])\s*분기",
        text
    )

    if year_quarter_match:
        year = int(year_quarter_match.group(1))
        quarter = int(year_quarter_match.group(2))
        return {
            "type": "year",
            "major": f"{year}년",
            "detail": f"{quarter}분기"
        }

    # "신규입사 3분기"처럼 연도 없이 분기만 적힌 값은
    # 신규입사 차수로 분류하지 않습니다.
    quarter_only_match = re.search(
        r"(?:^|\s|[\(\[])([1-4])\s*분기(?:$|\s|[\)\]])",
        text
    )

    new_hire_match = re.search(
        r"(\d+)\s*기",
        text
    )

    if quarter_only_match and "신규입사" in text:
        return {
            "type": "other",
            "major": "기타",
            "detail": text or "미분류"
        }

    if "신규입사" in text or new_hire_match:
        if new_hire_match:
            detail = f"{int(new_hire_match.group(1))}기"
        else:
            detail = text or "신규입사"

        return {
            "type": "new_hire",
            "major": "신규입사",
            "detail": detail
        }

    return {
        "type": "other",
        "major": "기타",
        "detail": text or "미분류"
    }


@st.cache_data(ttl=10, show_spinner=False)
def get_new_hire_batch_catalog():
    """신규입사 배분 이력을 계층형 선택기에 사용할 목록으로 가져옵니다."""

    result = (
        admin_supabase
        .table("new_hire_distribution_history")
        .select("quarter_id, batch_id, distribution_title")
        .order("created_at", desc=True)
        .execute()
    )

    rows = result.data or []
    unique = {}

    for row in rows:
        batch_id = row.get("batch_id")
        quarter_id = row.get("quarter_id")

        if not batch_id or not quarter_id:
            continue

        key = (str(quarter_id), str(batch_id))
        if key not in unique:
            parsed = parse_quarter_hierarchy_label(
                row.get("distribution_title")
            )
            unique[key] = {
                "quarter_id": quarter_id,
                "batch_id": batch_id,
                "distribution_title": row.get("distribution_title") or "신규입사",
                "type": parsed["type"],
                "major": parsed["major"],
                "detail": parsed["detail"]
            }

    return list(unique.values())


def build_hierarchical_quarter_options(
    quarters_data,
    include_new_hire=False,
    include_all=False
):
    """대분류 -> 세부 분류 구조와 실제 quarter_id/batch_id 매핑을 만듭니다."""

    major_details = {}
    detail_map = {}

    if include_all:
        major_details["전체"] = ["전체"]
        detail_map[("전체", "전체")] = {
            "quarter_id": None,
            "batch_id": None,
            "type": "all"
        }

    for quarter in quarters_data or []:
        major = f"{quarter['year']}년"
        detail = f"{quarter['quarter']}분기"

        major_details.setdefault(major, [])
        if detail not in major_details[major]:
            major_details[major].append(detail)

        detail_map[(major, detail)] = {
            "quarter_id": quarter["id"],
            "batch_id": None,
            "type": "year"
        }

    if include_new_hire:
        for batch in get_new_hire_batch_catalog():
            # 연도/분기로 해석되는 수기 입력값은 실제 분기 아래에서
            # quarter_id 기준으로 조회하고, 신규입사 대분류에는 넣지 않습니다.
            if batch.get("type") != "new_hire":
                continue

            major = batch["major"]
            detail = batch["detail"]

            major_details.setdefault(major, [])

            display_detail = detail
            suffix = 2
            while (major, display_detail) in detail_map:
                display_detail = f"{detail} ({suffix})"
                suffix += 1

            major_details[major].append(display_detail)
            detail_map[(major, display_detail)] = {
                "quarter_id": batch["quarter_id"],
                "batch_id": batch["batch_id"],
                "type": batch["type"]
            }

    # 최신 연도부터, 신규입사는 마지막에 배치합니다.
    def major_sort_key(value):
        if value == "전체":
            return (0, 0, value)
        if value == "신규입사":
            return (2, 0, value)
        year_match = re.match(r"(20\d{2})년$", value)
        if year_match:
            return (1, -int(year_match.group(1)), value)
        return (3, 0, value)

    majors = sorted(major_details.keys(), key=major_sort_key)

    for major in majors:
        if major == "전체":
            continue
        if major == "신규입사":
            major_details[major] = sorted(
                major_details[major],
                key=lambda value: (
                    0 if re.match(r"^\d+기", value) else 1,
                    int(re.match(r"^(\d+)", value).group(1))
                    if re.match(r"^(\d+)", value) else 9999,
                    value
                )
            )
        else:
            major_details[major] = sorted(
                major_details[major],
                key=lambda value: int(value.replace("분기", ""))
                if value.endswith("분기") and value[:-2].isdigit() else 9999
            )

    return majors, major_details, detail_map


def render_hierarchical_quarter_selector(
    quarters_data,
    *,
    label,
    major_key,
    detail_key,
    include_new_hire=False,
    include_all=False
):
    """기존 단일 분기 selectbox를 대분류/세부 분류 2단계 선택으로 표시합니다."""

    majors, major_details, detail_map = build_hierarchical_quarter_options(
        quarters_data,
        include_new_hire=include_new_hire,
        include_all=include_all
    )

    if not majors:
        return None, None, None, None

    container_key = f"hierarchical_selector_{major_key}"

    st.markdown(
        f"""
        <style>
        .st-key-{container_key} {{
            width: fit-content !important;
            max-width: 100% !important;
        }}
        .st-key-{container_key} [data-testid="stSelectbox"] {{
            width: fit-content !important;
            min-width: 110px !important;
            max-width: 220px !important;
        }}
        .st-key-{container_key} [data-testid="stSelectbox"] [data-baseweb="select"],
        .st-key-{container_key} [data-testid="stSelectbox"] [data-baseweb="select"] > div {{
            width: fit-content !important;
            min-width: 110px !important;
            max-width: 220px !important;
        }}
        .st-key-{container_key} [data-testid="stSelectbox"] label {{
            font-weight: 700 !important;
        }}
        </style>
        """,
        unsafe_allow_html=True
    )

    current_major = st.session_state.get(major_key)
    if current_major not in majors:
        current_major = majors[0]

    with st.container(key=container_key):
        st.caption(label)
        major_col, detail_col = st.columns([1, 1], gap="small")

        with major_col:
            selected_major = st.selectbox(
                "대분류",
                majors,
                index=majors.index(current_major),
                key=major_key
            )

        detail_options = major_details.get(selected_major, [])
        if not detail_options:
            return selected_major, None, None, None

        current_detail = st.session_state.get(detail_key)
        if current_detail not in detail_options:
            current_detail = detail_options[0]

        with detail_col:
            selected_detail = st.selectbox(
                "세부 분류",
                detail_options,
                index=detail_options.index(current_detail),
                key=detail_key
            )

    selected = detail_map.get(
        (selected_major, selected_detail),
        {}
    )

    return (
        selected_major,
        selected_detail,
        selected.get("quarter_id"),
        selected.get("batch_id")
    )


@st.cache_data(ttl=30)
def get_registered_users():
    result = (
        admin_supabase
        .table("users")
        .select(
            "id, name, employee_no, role, created_at"
        )
        .eq(
            "is_active",
            True
        )
        .order(
            "created_at"
        )
        .execute()
    )

    return result.data


def get_distribution_history_summary(quarter_id=None, batch_id=None):
    """실제 배분 이력(distribution_history)을 기준으로 처리내역을 집계합니다.

    핵심 원칙:
    - 1인당 배분수량은 order_items.per_user_quantity가 아니라
      실제 이력의 quantity 합계를 사용합니다.
    - 같은 분기에서 동일 상품이 여러 order_item_id로 기록되어도
      quarter_id + item_id 기준으로 하나로 합칩니다.
    - 전체 조회에서는 quarter_id를 절대 합쳐 버리지 않고
      분기별로 독립된 행을 유지합니다.
    - 신규입사 선택(batch_id 지정) 시에는 해당 batch만 조회합니다.
    """

    def read_with_retry(query_builder, attempts=3):
        """읽기 요청만 일시적인 HTTPX 소켓 오류에 한해 재시도합니다."""
        last_error = None

        for attempt in range(attempts):
            try:
                return query_builder.execute()
            except (
                httpx.ReadError,
                httpx.ConnectError,
                httpx.ConnectTimeout,
                httpx.ReadTimeout,
            ) as exc:
                last_error = exc
                if attempt < attempts - 1:
                    time.sleep(0.8 * (2 ** attempt))

        raise last_error
    history_query = (
        admin_supabase
        .table("distribution_history")
        .select(
            "quarter_id, order_item_id, user_id, item_id, quantity"
        )
    )

    if batch_id is None and quarter_id is not None:
        history_query = history_query.eq(
            "quarter_id",
            quarter_id
        )

    if batch_id is not None:
        history_rows = []
    else:
        history_result = read_with_retry(history_query)
        history_rows = history_result.data or []

    new_hire_query = (
        admin_supabase
        .table("new_hire_distribution_history")
        .select(
            "quarter_id, user_id, item_id, quantity, "
            "distribution_title, batch_id"
        )
    )

    if batch_id is not None:
        new_hire_query = new_hire_query.eq(
            "batch_id",
            batch_id
        )
    elif quarter_id is not None:
        new_hire_query = new_hire_query.eq(
            "quarter_id",
            quarter_id
        )

    new_hire_result = read_with_retry(new_hire_query)
    new_hire_rows = new_hire_result.data or []

    if not history_rows and not new_hire_rows:
        return {}

    item_ids = {
        row.get("item_id")
        for row in history_rows + new_hire_rows
        if row.get("item_id") is not None
    }

    item_map = {}

    if item_ids:
        items_query = (
            admin_supabase
            .table("items")
            .select(
                "id, product_code, item_name"
            )
            .in_(
                "id",
                list(item_ids)
            )
        )

        items_result = read_with_retry(items_query)

        item_map = {
            row["id"]: row
            for row in (items_result.data or [])
        }

    quarter_map = {
        row["id"]: row
        for row in (get_all_quarters() or [])
    }

    summary = {}

    def add_history_row(
        row,
        distribution_type,
        distribution_title=None
    ):
        quarter_key = row.get("quarter_id")
        item_id = row.get("item_id")
        user_id = row.get("user_id")

        try:
            quantity = int(row.get("quantity") or 0)
        except (TypeError, ValueError):
            quantity = 0

        if (
            quarter_key is None
            or item_id is None
            or quantity <= 0
        ):
            return

        item = item_map.get(item_id)

        if not item:
            return

        summary_key = (
            quarter_key,
            item_id
        )

        if summary_key not in summary:
            quarter = quarter_map.get(quarter_key) or {}

            summary[summary_key] = {
                "quarter_id": quarter_key,
                "item_id": item_id,
                "order_item_id": row.get("order_item_id"),
                "distribution_type": distribution_type,
                "distribution_title": (
                    distribution_title
                    or "정기배분"
                ),
                "item": item,
                "quarter_label": (
                    f"{quarter.get('year')}년 "
                    f"{quarter.get('quarter')}분기"
                    if (
                        quarter.get("year") is not None
                        and quarter.get("quarter") is not None
                    )
                    else "분기 미상"
                ),
                "total_quantity": 0,
                "user_ids": set(),
                "user_quantities": {},
                "source_types": set()
            }

        summary[summary_key]["total_quantity"] += quantity
        summary[summary_key]["source_types"].add(
            distribution_type
        )

        if user_id is not None:
            summary[summary_key]["user_ids"].add(user_id)
            summary[summary_key]["user_quantities"][user_id] = (
                summary[summary_key]["user_quantities"].get(
                    user_id,
                    0
                )
                + quantity
            )

        if distribution_type == "new_hire":
            title = str(
                distribution_title
                or ""
            ).strip()

            if title:
                existing_title = summary[
                    summary_key
                ].get(
                    "distribution_title"
                )

                if existing_title in (
                    None,
                    "",
                    "정기배분"
                ):
                    summary[
                        summary_key
                    ][
                        "distribution_title"
                    ] = title

    for row in history_rows:
        add_history_row(
            row,
            "regular",
            "정기배분"
        )

    for row in new_hire_rows:
        add_history_row(
            row,
            "new_hire",
            row.get("distribution_title")
            or "신규입사"
        )

    for row in summary.values():
        user_quantity_values = sorted({
            int(quantity)
            for quantity in row["user_quantities"].values()
        })

        if len(user_quantity_values) == 1:
            row["per_user_quantity"] = (
                user_quantity_values[0]
            )
            row["per_user_quantity_text"] = (
                f"{user_quantity_values[0]:,}개"
            )
        elif not user_quantity_values:
            row["per_user_quantity"] = 0
            row["per_user_quantity_text"] = "0개"
        else:
            row["per_user_quantity"] = None
            row["per_user_quantity_text"] = "혼합"

    return summary


@st.cache_data(ttl=30, show_spinner=False)
def get_users_by_ids(user_ids):
    """처리내역의 배분 인원 클릭 시 이름/사번을 조회합니다."""

    normalized_ids = [
        str(user_id)
        for user_id in (user_ids or [])
        if user_id is not None
    ]

    if not normalized_ids:
        return {}

    result = (
        admin_supabase
        .table("users")
        .select(
            "id, name, employee_no"
        )
        .in_(
            "id",
            normalized_ids
        )
        .execute()
    )

    return {
        str(row["id"]): row
        for row in (result.data or [])
    }


def show_delete_order_items(
    selected_order_item_ids
):

    st.warning(
        f"{len(selected_order_item_ids)}개 품목을 "
        "발주 품목에서 삭제하시겠습니까?"
    )

    confirm_col1, confirm_col2 = st.columns(2)

    with confirm_col1:

        if st.button(
            "삭제",
            type="primary",
            use_container_width=True,
            key="modal_delete_order_items"
        ):

            for order_item_id in selected_order_item_ids:

                (
                    admin_supabase
                    .table("order_items")
                    .delete()
                    .eq(
                        "id",
                        order_item_id
                    )
                    .execute()
                )

            st.success(
                f"{len(selected_order_item_ids)}개 품목이 "
                "삭제되었습니다."
            )

            safe_rerun()

@st.dialog("발주 내용 저장 완료")
def show_order_save_complete():

    st.success(
        "발주 내용이 저장되었습니다."
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):
        safe_rerun()

@st.dialog("입고 확정 완료")
def show_receive_complete(
    received_count
):

    st.success(
        f"{received_count}개 품목이 "
        "입고 확정되었습니다."
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):
        safe_rerun()

@st.dialog("폐기 요청 저장 완료")
def show_disposal_save_complete():

    st.success(
        "폐기 요청이 저장되었습니다."
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):
        safe_rerun()

@st.dialog("안내")
def show_user_notice(
    message
):

    st.warning(
        message
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):

        st.session_state.user_notice_dismissed = True

        safe_rerun()

@st.dialog("취합 요청")
def show_collection_save_message(
    success=True
):

    if success:

        st.success(
            "취합 요청이 저장되었습니다."
        )

    else:

        st.error(
            "취합 요청 저장에 실패했습니다. "
            "잠시 후 다시 시도해주세요."
        )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):

        safe_rerun()

@st.dialog("폐기 요청")
def show_disposal_quantity_warning():

    st.warning(
        "폐기 수량을 1 이상 입력해주세요."
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):

        safe_rerun()

@st.dialog("폐기 요청")
def show_disposal_approved_warning():

    st.warning(
        "이미 폐기 확정된 품목은 "
        "수정할 수 없습니다."
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):

        safe_rerun()

@st.dialog("사용자 추가")
def show_add_user_dialog():

    st.subheader("새로운 사용자 등록")

    employee_no = st.text_input(
        "사번",
        key="modal_new_user_employee_no"
    )

    name = st.text_input(
        "이름",
        key="modal_new_user_name"
    )

    st.markdown(
        """
        <style>
        /* 인원 추가 모달의 완료/취소 버튼만 동일한 스타일 적용 */
        .st-key-modal_add_user button,
        .st-key-modal_cancel_add_user button {
            background: #2e8b57 !important;
            background-color: #2e8b57 !important;
            border-color: #2e8b57 !important;
            color: #ffffff !important;
        }

        .st-key-modal_add_user button:hover,
        .st-key-modal_cancel_add_user button:hover {
            background: #26734a !important;
            background-color: #26734a !important;
            border-color: #26734a !important;
        }

        .st-key-modal_add_user button p,
        .st-key-modal_cancel_add_user button p {
            font-weight: 700 !important;
            color: #ffffff !important;
            position: relative !important;
            top: -1px !important;
            margin-top: -1px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    add_col1, add_col2 = st.columns(2)

    with add_col1:

        if st.button(
            "완료",
            type="primary",
            use_container_width=True,
            key="modal_add_user"
        ):

            if not employee_no or not name:

                st.error(
                    "사번과 이름을 모두 입력해주세요."
                )

            else:

                try:

                    duplicate_result = (
                        admin_supabase
                        .table("users")
                        .select(
                            "id, name, employee_no, is_active"
                        )
                        .eq(
                            "employee_no",
                            employee_no
                        )
                        .limit(1)
                        .execute()
                    )

                    if duplicate_result.data:

                        existing_user = (
                            duplicate_result.data[0]
                        )

                        if existing_user["name"] == name:

                            st.error(
                                "이미 등록된 인원입니다."
                            )

                        else:

                            st.error(
                                "이미 등록된 사번입니다."
                            )

                    else:

                        admin_supabase.table(
                            "users"
                        ).insert(
                            {
                                "name": name,
                                "employee_no": employee_no,
                                "role": "user",
                                "is_active": True
                            }
                        ).execute()

                        get_registered_users.clear()

                        st.session_state.pop(
                            "modal_new_user_employee_no",
                            None
                        )

                        st.session_state.pop(
                            "modal_new_user_name",
                            None
                        )

                        st.success(
                            f"{name}님이 추가되었습니다."
                        )

                        safe_rerun()

                except Exception:

                    st.error(
                        "사용자 정보를 저장할 수 없습니다. "
                        "입력 내용을 확인해주세요."
                    )

    with add_col2:

        if st.button(
            "취소",
            use_container_width=True,
            key="modal_cancel_add_user"
        ):

            safe_rerun()

@st.dialog("인원 정보 수정")
def show_edit_user_dialog(
    edit_user
):

    edit_user_id = edit_user["id"]

    edit_employee_no = st.text_input(
        "사번",
        value=edit_user["employee_no"],
        key=f"modal_edit_employee_no_{edit_user_id}"
    )

    edit_name = st.text_input(
        "이름",
        value=edit_user["name"],
        key=f"modal_edit_name_{edit_user_id}"
    )

    if st.session_state.get(
        "confirm_delete_user_id"
    ) == edit_user_id:

        st.warning(
            f"'{edit_user['name']}님을 "
            "삭제하시겠습니까?"
        )

        delete_col1, delete_col2 = st.columns(2)

        with delete_col1:

            if st.button(
                "삭제 확정",
                type="primary",
                use_container_width=True,
                key=f"modal_confirm_delete_{edit_user_id}"
            ):

                try:

                    admin_supabase.table(
                        "users"
                    ).update(
                        {
                            "is_active": False
                        }
                    ).eq(
                        "id",
                        edit_user_id
                    ).execute()

                    get_registered_users.clear()

                    st.session_state.pop(
                        "confirm_delete_user_id",
                        None
                    )

                    st.session_state.pop(
                        "edit_user_id",
                        None
                    )

                    safe_rerun()

                except Exception:

                    st.error(
                        "인원 삭제에 실패했습니다."
                    )

        with delete_col2:

            if st.button(
                "취소",
                use_container_width=True,
                key=f"modal_cancel_delete_{edit_user_id}"
            ):

                st.session_state.pop(
                    "confirm_delete_user_id",
                    None
                )

                safe_rerun()

    else:

        edit_col1, edit_col2, edit_col3 = st.columns(3)

        with edit_col1:

            if st.button(
                "저장",
                type="primary",
                use_container_width=True,
                key=f"modal_save_user_{edit_user_id}"
            ):

                if not edit_employee_no or not edit_name:

                    st.error(
                        "사번과 이름을 모두 입력해주세요."
                    )

                else:

                    try:

                        duplicate_result = (
                            admin_supabase
                            .table("users")
                            .select("id")
                            .eq(
                                "employee_no",
                                edit_employee_no
                            )
                            .neq(
                                "id",
                                edit_user_id
                            )
                            .limit(1)
                            .execute()
                        )

                        if duplicate_result.data:

                            st.error(
                                "이미 등록된 사번입니다."
                            )

                        else:

                            admin_supabase.table(
                                "users"
                            ).update(
                                {
                                    "employee_no":
                                        edit_employee_no,
                                    "name":
                                        edit_name
                                }
                            ).eq(
                                "id",
                                edit_user_id
                            ).execute()

                            get_registered_users.clear()

                            st.session_state.pop(
                                "edit_user_id",
                                None
                            )

                            safe_rerun()

                    except Exception:

                        st.error(
                            "인원 정보 저장에 실패했습니다."
                        )

        with edit_col2:

            if st.button(
                "삭제",
                use_container_width=True,
                key=f"modal_delete_user_{edit_user_id}"
            ):

                st.session_state[
                    "confirm_delete_user_id"
                ] = edit_user_id

                safe_rerun()

        with edit_col3:

            if st.button(
                "취소",
                use_container_width=True,
                key=f"modal_cancel_edit_user_{edit_user_id}"
            ):

                st.session_state.pop(
                    "edit_user_id",
                    None
                )

                safe_rerun()

@st.dialog("상품 일괄 등록", width="large")
def show_add_items_dialog(
    categories
):

    dialog_version = st.session_state.get(
        "bulk_item_dialog_version",
        0
    )

    if st.session_state.get(
        "bulk_item_save_complete",
        False
    ):

        st.success(
            st.session_state.get(
                "bulk_item_save_message",
                "상품 등록이 완료되었습니다."
            )
        )

        if st.session_state.get(
            "bulk_item_save_failed"
        ):

            st.error(
                "일부 상품은 등록하지 못했습니다."
            )

            for message in st.session_state.get(
                "bulk_item_save_failed",
                []
            ):

                st.write(
                    f"• {message}"
                )

        if st.button(
            "확인",
            type="primary",
            use_container_width=True,
            key=(
                f"bulk_item_save_confirm_"
                f"{dialog_version}"
            )
        ):

            st.session_state.bulk_item_save_complete = (
                False
            )

            st.session_state.pop(
                "bulk_item_save_message",
                None
            )

            st.session_state.pop(
                "bulk_item_save_failed",
                None
            )

            safe_rerun()

        return

    st.write(
        "엑셀에서 매장명, 상품코드, 상품명, 원가를 "
        "복사하여 붙여넣어 주세요."
    )

    pasted_text = st.text_area(
        "엑셀 데이터",
        height=150,
        placeholder=(
            "매장명\t상품코드\t상품명\t원가\n"
            "강남점\tA001\t립밤A\t10000\n"
            "성수점\tA002\t파운데이션B\t18000"
        ),
        key=(
            f"bulk_item_pasted_text_"
            f"{dialog_version}"
        )
    )

    if not pasted_text.strip():

        st.info(
            "엑셀에서 매장명, 상품코드, 상품명, 원가를 "
            "복사하여 붙여넣어 주세요."
        )

        return

    rows = []

    rows_state_key = (
        f"bulk_item_rows_{dialog_version}"
    )

    source_state_key = (
        f"bulk_item_source_{dialog_version}"
    )

    if (
        st.session_state.get(
            source_state_key
        )
        != pasted_text
    ):

        parsed_rows = []

        for index, line in enumerate(
            pasted_text.strip().splitlines()
        ):

            columns = line.split("\t")

            if len(columns) < 4:

                continue

            store_name = columns[0].strip()
            product_code = columns[1].strip()
            item_name = columns[2].strip()
            cost_price = columns[3].strip()

            if (
                store_name == "매장명"
                and product_code == "상품코드"
                and item_name == "상품명"
            ):

                continue

            parsed_rows.append(
                {
                    "row_id": index,
                    "store_name": store_name,
                    "product_code": product_code,
                    "item_name": item_name,
                    "cost_price": cost_price
                }
            )

        st.session_state[
            rows_state_key
        ] = parsed_rows

        st.session_state[
            source_state_key
        ] = pasted_text

    rows = st.session_state.get(
        rows_state_key,
        []
    )

    if not rows:

        st.warning(
            "붙여넣은 상품 정보를 확인해주세요."
        )

        return

    st.write(
        f"총 {len(rows)}개 상품"
    )

    st.divider()

    with st.container(
        height=550,
        border=False
    ):

        header_col1, header_col2, header_col3, header_col4, header_col5, header_col6, header_col7, header_col8 = (
            st.columns(
                [1.5, 1.5, 2.5, 1.2, 1.6, 1.6, 1.8, 0.8]
            )
        )

        with header_col1:

            st.write("매장명")

        with header_col2:

            st.write("상품코드")

        with header_col3:

            st.write("상품명")

        with header_col4:

            st.write("원가")

        with header_col5:

            st.write("대분류")

        with header_col6:

            st.write("소분류")

        with header_col7:

            st.write("사진")

        with header_col8:

            st.write("삭제")

        st.divider()

        prepared_rows = []

        for row in rows:

            row_id = row["row_id"]

            col1, col2, col3, col4, col5, col6, col7, col8 = (
                st.columns(
                    [1.5, 1.5, 2.5, 1.2, 1.6, 1.6, 1.8, 0.8]
                )
            )

            with col1:

                st.write(
                    row["store_name"]
                )

            with col2:

                st.write(
                    row["product_code"]
                )

            with col3:

                st.write(
                    row["item_name"]
                )

            with col4:

                try:

                    display_cost = (
                        f"{int(row['cost_price'].replace(',', '').strip()):,}"
                    )

                except Exception:

                    display_cost = row["cost_price"]

                st.write(
                    display_cost
                )

            with col5:

                selected_major_name = st.selectbox(
                    "대분류",
                    list(
                        major_category_options.keys()
                    ),
                    key=(
                        f"bulk_major_category_"
                        f"{dialog_version}_"
                        f"{row_id}"
                    ),
                    label_visibility="collapsed"
                )

            selected_major_id = (
                major_category_options[
                    selected_major_name
                ]
            )

            sub_categories = [
                category
                for category in categories
                if (
                    category["parent_id"]
                    == selected_major_id
                )
            ]

            selected_category_id = (
                selected_major_id
            )

            with col6:

                if sub_categories:

                    sub_category_options = {
                        category["category_name"]:
                        category["id"]
                        for category in sub_categories
                    }

                    selected_sub_name = st.selectbox(
                        "소분류",
                        list(
                            sub_category_options.keys()
                        ),
                        key=(
                            f"bulk_sub_category_"
                            f"{dialog_version}_"
                            f"{row_id}"
                        ),
                        label_visibility="collapsed"
                    )

                    selected_category_id = (
                        sub_category_options[
                            selected_sub_name
                        ]
                    )

                else:

                    st.write("-")

            with col7:

                image_file = st.file_uploader(
                    "사진",
                    type=[
                        "jpg",
                        "jpeg",
                        "png",
                        "webp"
                    ],
                    key=(
                        f"bulk_item_image_"
                        f"{dialog_version}_"
                        f"{row_id}"
                    ),
                    label_visibility="collapsed"
                )

            with col8:

                if st.button(
                    "삭제",
                    key=(
                        f"bulk_delete_row_"
                        f"{dialog_version}_"
                        f"{row_id}"
                    ),
                    use_container_width=True
                ):

                    st.session_state[
                        rows_state_key
                    ] = [
                        existing_row
                        for existing_row in rows
                        if existing_row["row_id"]
                        != row_id
                    ]

                    st.rerun(
                        scope="fragment"
                    )

            prepared_rows.append(
                {
                    "store_name":
                        row["store_name"],
                    "product_code":
                        row["product_code"],
                    "item_name":
                        row["item_name"],
                    "cost_price":
                        row["cost_price"],
                    "category_id":
                        selected_category_id,
                    "image_file":
                        image_file
                }
            )

            if row_id != rows[-1]["row_id"]:

                st.divider()

    st.divider()

    button_col1, button_col2 = st.columns(2)

    with button_col1:

        save_button = st.button(
            "일괄 등록",
            type="primary",
            use_container_width=True,
            key=(
                f"bulk_item_save_"
                f"{dialog_version}"
            )
        )

    with button_col2:

        cancel_button = st.button(
            "취소",
            use_container_width=True,
            key=(
                f"bulk_item_cancel_"
                f"{dialog_version}"
            )
        )

    if cancel_button:

        safe_rerun()

    if save_button:

        validation_errors = []

        product_codes = [
            row["product_code"]
            for row in prepared_rows
        ]

        # 기본 입력값 확인

        seen_codes = set()

        for row in prepared_rows:

            if not row["store_name"]:

                validation_errors.append(
                    "매장명이 입력되지 않은 행이 있습니다."
                )

            if not row["product_code"]:

                validation_errors.append(
                    "상품코드가 입력되지 않은 행이 있습니다."
                )

            if not row["item_name"]:

                validation_errors.append(
                    "상품명이 입력되지 않은 행이 있습니다."
                )

            if not row["cost_price"]:

                validation_errors.append(
                    (
                        f"{row['product_code'] or '상품코드 없음'}: "
                        "원가가 입력되지 않았습니다."
                    )
                )

            else:

                try:

                    int(
                        row["cost_price"]
                        .replace(",", "")
                        .strip()
                    )

                except Exception:

                    validation_errors.append(
                        (
                            f"{row['product_code']}: "
                            "원가가 숫자가 아닙니다."
                        )
                    )

            if row["product_code"] in seen_codes:

                validation_errors.append(
                    (
                        f"{row['product_code']}: "
                        "붙여넣은 데이터 안에서 "
                        "상품코드가 중복되었습니다."
                    )
                )

            seen_codes.add(
                row["product_code"]
            )

            if not row["image_file"]:

                validation_errors.append(
                    (
                        f"{row['product_code']}: "
                        "상품 사진을 선택해주세요."
                    )
                )

        if validation_errors:

            for message in validation_errors:

                st.error(
                    message
                )

        else:

            # 기존 상품코드 중복 확인

            existing_result = (
                admin_supabase
                .table("items")
                .select(
                    "id, product_code, is_active"
                )
                .in_(
                    "product_code",
                    product_codes
                )
                .execute()
            )

            existing_active_codes = {
                row["product_code"]
                for row in (
                    existing_result.data
                    or []
                )
                if row.get("is_active")
            }

            inactive_items = {
                row["product_code"]: row["id"]
                for row in (
                    existing_result.data
                    or []
                )
                if not row.get("is_active")
            }

            if existing_active_codes:

                for code in sorted(
                    existing_active_codes
                ):

                    st.error(
                        (
                            f"{code}: "
                            "이미 등록된 상품코드입니다."
                        )
                    )

            else:

                current_quarter_result = (
                    admin_supabase
                    .table("quarters")
                    .select("id")
                    .eq(
                        "status",
                        "collecting"
                    )
                    .order(
                        "year",
                        desc=True
                    )
                    .order(
                        "quarter",
                        desc=True
                    )
                    .limit(1)
                    .execute()
                )

                current_quarter_id = None

                if current_quarter_result.data:

                    current_quarter_id = (
                        current_quarter_result
                        .data[0]["id"]
                    )

                success_count = 0
                failed_messages = []

                for row in prepared_rows:

                    try:

                        image = Image.open(
                            row["image_file"]
                        )

                        if image.mode != "RGB":

                            image = image.convert(
                                "RGB"
                            )

                        width, height = (
                            image.size
                        )

                        size = min(
                            width,
                            height
                        )

                        left = (
                            width - size
                        ) // 2

                        top = (
                            height - size
                        ) // 2

                        right = (
                            left + size
                        )

                        bottom = (
                            top + size
                        )

                        image = image.crop(
                            (
                                left,
                                top,
                                right,
                                bottom
                            )
                        )

                        image.thumbnail(
                            (600, 600),
                            Image.Resampling.LANCZOS
                        )

                        image_bytes = (
                            io.BytesIO()
                        )

                        image.save(
                            image_bytes,
                            format="JPEG",
                            quality=80,
                            optimize=True,
                            progressive=True
                        )

                        image_bytes.seek(0)

                        file_path = (
                            f"{row['product_code']}.jpg"
                        )

                        admin_supabase.storage.from_(
                            "item-images"
                        ).upload(
                            file_path,
                            image_bytes.getvalue(),
                            {
                                "content-type":
                                    "image/jpeg",
                                "upsert":
                                    "true"
                            }
                        )

                        cost_price = int(
                            row["cost_price"]
                            .replace(",", "")
                            .strip()
                        )

                        item_data = {
                            "store_name":
                                row["store_name"],
                            "product_code":
                                row["product_code"],
                            "item_name":
                                row["item_name"],
                            "category_id":
                                row["category_id"],
                            "image_path":
                                file_path,
                            "cost_price":
                                cost_price,
                            "is_active":
                                True
                        }

                        inactive_item_id = inactive_items.get(
                            row["product_code"]
                        )

                        if inactive_item_id:

                            new_item_result = (
                                admin_supabase
                                .table("items")
                                .update(item_data)
                                .eq(
                                    "id",
                                    inactive_item_id
                                )
                                .execute()
                            )

                        else:

                            new_item_result = (
                                admin_supabase
                                .table("items")
                                .insert(item_data)
                                .execute()
                            )

                        new_item = (
                            new_item_result
                            .data[0]
                        )

                        if current_quarter_id:

                            admin_supabase.table(
                                "quarter_items"
                            ).upsert(
                                {
                                    "quarter_id":
                                        current_quarter_id,
                                    "item_id":
                                        new_item["id"],
                                    "distribution_available":
                                        True,
                                    "disposal_available":
                                        True
                                },
                                on_conflict=(
                                    "quarter_id,item_id"
                                )
                            ).execute()

                        success_count += 1

                    except Exception:

                        failed_messages.append(
                            (
                                f"{row['product_code']}: "
                                "등록에 실패했습니다."
                            )
                        )

                st.session_state.bulk_item_save_complete = (
                    True
                )

                st.session_state.bulk_item_save_message = (
                    f"{success_count}개 상품이 등록되었습니다."
                )

                st.session_state.bulk_item_save_failed = (
                    failed_messages
                )

                safe_rerun()

@st.dialog("분기 생성")
def show_create_quarter_dialog():

    st.write(
        "새로운 취합 분기를 생성합니다."
    )

    create_col1, create_col2 = st.columns(2)

    with create_col1:

        year = st.number_input(
            "연도",
            min_value=2026,
            max_value=2100,
            value=2026,
            step=1,
            key="modal_create_year"
        )

    with create_col2:

        quarter = st.selectbox(
            "분기",
            [1, 2, 3, 4],
            key="modal_create_quarter_number"
        )

    create_col3, create_col4 = st.columns(2)

    with create_col3:

        start_date = st.date_input(
            "취합 시작일",
            key="modal_create_start_date"
        )

    with create_col4:

        end_date = st.date_input(
            "취합 마감일",
            key="modal_create_end_date"
        )

    st.divider()

    button_col1, button_col2 = st.columns(
        2,
        vertical_alignment="bottom"
    )

    with button_col1:

        st.markdown(
            """
            <style>
            [class*="st-key-modal_create_quarter"] button,
            [class*="st-key-modal_cancel_quarter"] button {
                background: #2e7d32 !important;
                background-color: #2e7d32 !important;
                color: #ffffff !important;
                font-weight: 800 !important;
                font-size: 16px !important;
                padding: 10px 20px !important;
                min-height: 44px !important;
                height: 44px !important;
                border: none !important;
                border-radius: 8px !important;
                box-sizing: border-box !important;
            }
            [class*="st-key-modal_create_quarter"] button:hover,
            [class*="st-key-modal_cancel_quarter"] button:hover {
                background: #267326 !important;
                background-color: #267326 !important;
                color: #ffffff !important;
            }
            [class*="st-key-modal_create_quarter"] button p,
            [class*="st-key-modal_cancel_quarter"] button p {
                color: #ffffff !important;
                font-weight: 800 !important;
                font-size: 16px !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        create_button = st.button(
            "분기 생성",
            type="primary",
            use_container_width=True,
            key="modal_create_quarter"
        )

    with button_col2:

        cancel_button = st.button(
            "취소",
            use_container_width=True,
            key="modal_cancel_quarter"
        )

    if cancel_button:

        safe_rerun()

    if create_button:

        if end_date < start_date:

            st.error(
                "마감일은 시작일보다 빠를 수 없습니다."
            )

        else:

            try:

                # 현재 취합중인 분기는 생성 후 마감 처리하고,
                # 신규 분기의 품목 설정은 가장 최근 분기에서 상속
                old_quarter = get_current_quarter()

                latest_quarter_result = (
                    admin_supabase
                    .table("quarters")
                    .select("id, year, quarter, status")
                    .order("year", desc=True)
                    .order("quarter", desc=True)
                    .limit(1)
                    .execute()
                )

                latest_quarter = (
                    latest_quarter_result.data[0]
                    if latest_quarter_result.data
                    else None
                )

                previous_item_settings = {}

                if latest_quarter:

                    previous_settings_result = (
                        admin_supabase
                        .table("quarter_items")
                        .select(
                            "item_id, distribution_available, disposal_available"
                        )
                        .eq(
                            "quarter_id",
                            latest_quarter["id"]
                        )
                        .execute()
                    )

                    previous_item_settings = {
                        row["item_id"]: row
                        for row in previous_settings_result.data
                    }

                # 새 분기 생성
                new_quarter_result = (
                    admin_supabase
                    .table("quarters")
                    .insert({
                        "year": year,
                        "quarter": quarter,
                        "start_date": str(start_date),
                        "end_date": str(end_date),
                        "status": "collecting"
                    })
                    .execute()
                )

                if new_quarter_result.data:

                    new_quarter_id = (
                        new_quarter_result.data[0]["id"]
                    )

                    # 새 분기 품목 설정 생성
                    # 이전 분기 설정이 있으면 그대로 복사하고,
                    # 새로 추가된 품목은 기본값(True)으로 생성
                    active_items_result = (
                        admin_supabase
                        .table("items")
                        .select("id")
                        .eq("is_active", True)
                        .execute()
                    )

                    new_quarter_item_settings = []

                    for item in active_items_result.data:

                        item_id = item["id"]
                        previous_setting = previous_item_settings.get(
                            item_id,
                            {}
                        )

                        new_quarter_item_settings.append({
                            "quarter_id": new_quarter_id,
                            "item_id": item_id,
                            "distribution_available": previous_setting.get(
                                "distribution_available",
                                True
                            ),
                            "disposal_available": previous_setting.get(
                                "disposal_available",
                                True
                            )
                        })

                    if new_quarter_item_settings:

                        admin_supabase.table(
                            "quarter_items"
                        ).upsert(
                            new_quarter_item_settings,
                            on_conflict="quarter_id,item_id"
                        ).execute()

                    # 기존 취합중 분기가 있으면
                    # 취합용 데이터만 정리
                    if old_quarter:

                        old_quarter_id = old_quarter["id"]

                        # 기존 분기 취합 데이터 삭제
                        admin_supabase.table(
                            "requests"
                        ).delete().eq(
                            "quarter_id",
                            old_quarter_id
                        ).execute()

                        # 기존 분기 상품 설정 삭제
                        admin_supabase.table(
                            "quarter_items"
                        ).delete().eq(
                            "quarter_id",
                            old_quarter_id
                        ).execute()

                        # 기존 분기 발주 데이터 삭제
                        # order_items는 CASCADE로 자동 삭제
                        admin_supabase.table(
                            "orders"
                        ).delete().eq(
                            "quarter_id",
                            old_quarter_id
                        ).execute()

                        # 기존 분기 마감
                        admin_supabase.table(
                            "quarters"
                        ).update({
                            "status": "closed"
                        }).eq(
                            "id",
                            old_quarter_id
                        ).execute()

                # 분기 목록/현재 분기 캐시 갱신
                get_current_quarter.clear()
                get_all_quarters.clear()

                st.session_state[
                    "quarter_create_complete"
                ] = True

                st.session_state[
                    "quarter_create_message"
                ] = (
                    f"{year}년 {quarter}분기가 "
                    "생성되었습니다."
                )

                safe_rerun()

            except Exception as e:

                st.error(
                    f"분기 생성에 실패했습니다: {e}"
                )

@st.dialog("분기 관리", width="small")
def show_quarter_manage_dialog(
    quarter_data
):

    quarter_id = quarter_data["id"]

    st.subheader(
        f"{quarter_data['year']}년 "
        f"{quarter_data['quarter']}분기"
    )

    st.divider()

    # 일정 수정

    st.write("일정 수정")

    manage_col1, manage_col2 = st.columns(2)

    with manage_col1:

        manage_start_date = st.date_input(
            "취합 시작일",
            value=date.fromisoformat(
                quarter_data["start_date"]
            ),
            key=f"modal_manage_start_{quarter_id}"
        )

    with manage_col2:

        manage_end_date = st.date_input(
            "취합 마감일",
            value=date.fromisoformat(
                quarter_data["end_date"]
            ),
            key=f"modal_manage_end_{quarter_id}"
        )

    st.divider()

    # 분기 삭제

    st.write("분기 삭제")

    delete_confirm = st.checkbox(
        "이 분기를 삭제하겠습니다.",
        key=f"modal_delete_confirm_{quarter_id}"
    )

    # 일정 저장 / 분기 삭제 버튼 영역만 컴팩트 + 우측 정렬
    with st.container(key="quarter_manage_button_row"):

        st.markdown(
            """
            <style>
            /* 분기 관리 모달의 일정 저장 / 분기 삭제 버튼만 대상 */
            .st-key-quarter_manage_button_row [data-testid="stHorizontalBlock"] {
                display: flex !important;
                justify-content: flex-end !important;
                align-items: center !important;
                gap: 8px !important;
            }

            .st-key-quarter_manage_button_row [data-testid="stHorizontalBlock"] > div {
                flex: 0 0 auto !important;
                width: auto !important;
            }

            .st-key-quarter_manage_button_row [data-testid="stButton"] {
                display: flex !important;
                justify-content: flex-end !important;
                align-items: center !important;
                width: auto !important;
                margin: 0 !important;
            }

            .st-key-quarter_manage_button_row [data-testid="stButton"] > button {
                width: auto !important;
                min-width: 0 !important;
                max-width: none !important;
                flex: 0 0 auto !important;
                display: inline-flex !important;
                align-items: center !important;
                margin: 0 !important;
                padding: 8px 16px !important;
                font-weight: 700 !important;
                box-sizing: border-box !important;
            }

            .st-key-quarter_manage_button_row [data-testid="stButton"] button p {
                margin-top: -1px !important;
                margin-bottom: 0 !important;
                font-weight: 700 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        button_spacer, schedule_button_col, delete_button_col = st.columns(
            [8, 1, 1],
            gap="small"
        )

        with schedule_button_col:
            schedule_save_button = st.button(
                "일정 저장",
                type="primary",
                width="content",
                key=f"modal_save_schedule_{quarter_id}"
            )

        with delete_button_col:
            delete_quarter_button = st.button(
                "분기 삭제",
                width="content",
                key=f"modal_delete_quarter_{quarter_id}"
            )

    if schedule_save_button:

        if manage_end_date < manage_start_date:

            st.error(
                "마감일은 시작일보다 빠를 수 없습니다."
            )

        else:

            try:

                today = date.today()

                if manage_start_date <= today <= manage_end_date:
                    updated_status = "collecting"
                elif today > manage_end_date:
                    updated_status = "closed"
                else:
                    updated_status = quarter_data.get(
                        "status",
                        "closed"
                    )

                admin_supabase.table(
                    "quarters"
                ).update({
                    "start_date": str(
                        manage_start_date
                    ),
                    "end_date": str(
                        manage_end_date
                    ),
                    "status": updated_status
                }).eq(
                    "id",
                    quarter_id
                ).execute()

                get_current_quarter.clear()
                get_all_quarters.clear()

                st.session_state[
                    "quarter_manage_message"
                ] = "일정이 수정되었습니다."

                safe_rerun()

            except Exception:

                st.error(
                    "일정 수정 실패"
                )

    if delete_quarter_button:

        if not delete_confirm:

            st.warning(
                "삭제 확인을 체크해주세요."
            )

        else:

            try:

                admin_supabase.table(
                    "requests"
                ).delete().eq(
                    "quarter_id",
                    quarter_id
                ).execute()

                admin_supabase.table(
                    "disposals"
                ).delete().eq(
                    "quarter_id",
                    quarter_id
                ).execute()

                admin_supabase.table(
                    "orders"
                ).delete().eq(
                    "quarter_id",
                    quarter_id
                ).execute()

                admin_supabase.table(
                    "quarter_items"
                ).delete().eq(
                    "quarter_id",
                    quarter_id
                ).execute()

                admin_supabase.table(
                    "quarters"
                ).delete().eq(
                    "id",
                    quarter_id
                ).execute()

                st.session_state[
                    "quarter_manage_message"
                ] = "분기가 삭제되었습니다."

                safe_rerun()

            except Exception:

                st.error(
                    "분기 삭제 실패"
                )

@st.dialog("품목별 취합 설정")
def show_item_setting_save_complete():

    st.success(
        "품목별 취합 설정이 저장되었습니다."
    )

    if st.button(
        "확인",
        type="primary",
        use_container_width=True
    ):

        safe_rerun()

def show_new_hire_distribution_ui(selected_quarter_id):
    """신규입사 전용 일괄 배분 UI.

    기존 정기 발주/배분 로직과 분리된 독립 UI이며,
    상품코드 → 품목 매칭 → 분기 배분 가능 여부 확인 → 사용자 선택 →
    상품별 수량 입력 → 신규입사 이력/보유수량 반영 순서로 처리한다.
    """

    with st.container(key="new_hire_distribution_ui"):

        st.markdown("### 신규입사")

        st.markdown(
            """
            <style>
            /* 신규입사 영역 내부에만 적용 */
            .st-key-new_hire_distribution_ui div[data-testid="stMultiSelect"] {
                width: fit-content !important;
                min-width: 220px !important;
                max-width: 360px !important;
            }

            .st-key-new_hire_distribution_ui div[data-testid="stTextInput"] {
                width: 280px !important;
                min-width: 280px !important;
                max-width: 280px !important;
            }

            .st-key-new_hire_distribution_ui div[data-testid="stTextArea"] {
                width: 380px !important;
                min-width: 380px !important;
                max-width: 380px !important;
            }

            .st-key-new_hire_distribution_ui textarea {
                width: 380px !important;
                max-width: 380px !important;
            }

            .st-key-new_hire_distribution_ui div[data-testid="stNumberInput"] {
                width: 72px !important;
                min-width: 72px !important;
                max-width: 72px !important;
            }

            .st-key-new_hire_distribution_ui div[data-testid="stNumberInput"] input {
                width: 72px !important;
                text-align: center !important;
            }

            .st-key-new_hire_distribution_ui .new-hire-warning {
                color: #d93025;
                font-weight: 700;
                white-space: nowrap;
                font-size: 13px;
            }

            .st-key-new_hire_distribution_ui .new-hire-ok {
                color: #188038;
                font-weight: 700;
                white-space: nowrap;
                font-size: 13px;
            }

            .st-key-new_hire_save_button div[data-testid="stButton"] > button {
                width: max-content !important;
                min-width: max-content !important;
                max-width: max-content !important;
                white-space: nowrap !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        # --------------------------------------------------
        # 1. 배분 차수/명칭
        # --------------------------------------------------
        distribution_title = st.text_input(
            "배분 차수 / 명칭",
            value=st.session_state.get(
                "new_hire_distribution_title",
                "신규입사(N기)"
            ),
            key="new_hire_distribution_title",
            placeholder="예: 신규입사(5기) / 2026년 4분기"
        )

        # --------------------------------------------------
        # 1-1. 실제 배분 기준 분기 확정
        # --------------------------------------------------
        # 명칭에 연도+분기가 직접 들어오면 현재 메인 분기보다
        # 해당 수기 입력값의 quarter_id를 절대 우선 적용합니다.
        target_quarter_id = resolve_new_hire_target_quarter_id(
            distribution_title,
            fallback_quarter_id=selected_quarter_id
        )

        title_has_year_quarter = bool(
            re.search(
                r"20\d{2}\s*년?\s*[1-4]\s*분기",
                distribution_title
            )
        )
        compact_title = re.sub(
            r"\s+",
            "",
            distribution_title
        )
        title_has_quarter_only = bool(
            not title_has_year_quarter
            and re.search(
                r"(?<!\d)[1-4]분기",
                compact_title
            )
        )

        # 연도+분기를 직접 입력한 경우에는 현재 메인 분기와의
        # 일치 여부를 검사하지 않습니다.
        # resolve_new_hire_target_quarter_id()가 수기 입력 분기를 기준으로
        # 기존 quarter를 찾거나 reference quarter를 자동 생성합니다.
        if title_has_year_quarter and target_quarter_id is None:
            st.error(
                "입력한 연도/분기를 배분 기준으로 설정하지 못했습니다. "
                "현재 메인 분기로 대체하지 않았습니다."
            )
            return

        if (
            not title_has_year_quarter
            and title_has_quarter_only
        ):
            st.error(
                "분기를 직접 입력할 때는 연도까지 입력해주세요. "
                "예: 2026년 3분기"
            )
            return

        if target_quarter_id is None:
            st.error(
                "배분 기준 분기를 확인할 수 없습니다. "
                "등록된 분기 또는 예: 2026년 3분기 형식으로 입력해주세요."
            )
            return

        if title_has_year_quarter:
            target_quarter = next(
                (
                    row
                    for row in (get_all_quarters() or [])
                    if row.get("id") == target_quarter_id
                ),
                None
            )
            if target_quarter:
                st.caption(
                    "배분 기준 분기: "
                    f"{target_quarter.get('year')}년 "
                    f"{target_quarter.get('quarter')}분기 "
                    "(수기 입력값 적용)"
                )

        # --------------------------------------------------
        # 2. 신규입사자 선택
        # --------------------------------------------------
        registered_users = get_registered_users() or []

        user_options = {
            f"{user.get('name', '-')}({user.get('employee_no', '-')})": user
            for user in registered_users
        }

        selected_user_labels = st.multiselect(
            "배분 인원",
            options=list(user_options.keys()),
            key="new_hire_selected_user_labels",
            placeholder="인원 선택",
            help="신규입사자를 여러 명 선택하면 동일한 상품/수량이 각 인원에게 일괄 배분됩니다."
        )

        selected_users = [
            user_options[label]
            for label in selected_user_labels
            if label in user_options
        ]

        # --------------------------------------------------
        # 3. 상품코드 붙여넣기
        # --------------------------------------------------
        pasted_text = st.text_area(
            "상품코드",
            height=100,
            placeholder=(
                "엑셀에서 상품코드 열만 복사하여 붙여넣으세요.\n"
                "예:\n"
                "A001\n"
                "A002\n"
                "A003"
            ),
            key="new_hire_pasted_text"
        )

        if not pasted_text.strip():
            st.info("엑셀에서 상품코드 열만 복사하여 붙여넣어 주세요.")
            return

        # --------------------------------------------------
        # 4. 상품코드 파싱
        # --------------------------------------------------
        source_key = "new_hire_pasted_source"
        rows_key = "new_hire_pasted_rows"

        if st.session_state.get(source_key) != pasted_text:
            parsed_rows = []
            seen_codes = set()

            for index, line in enumerate(
                pasted_text.strip().splitlines(),
                start=1
            ):
                product_code = line.split("\t")[0].strip()

                if not product_code:
                    continue

                if product_code.lower() in {
                    "상품코드",
                    "product code",
                    "product_code"
                }:
                    continue

                if product_code in seen_codes:
                    continue

                seen_codes.add(product_code)
                parsed_rows.append({
                    "row_id": index,
                    "product_code": product_code
                })

            st.session_state[rows_key] = parsed_rows
            st.session_state[source_key] = pasted_text

        pasted_rows = st.session_state.get(rows_key, [])

        if not pasted_rows:
            st.warning("입력된 상품코드를 확인해주세요.")
            return

        product_codes = [
            row["product_code"]
            for row in pasted_rows
        ]

        # --------------------------------------------------
        # 5. 상품코드 → 상품 매칭
        # --------------------------------------------------
        # 신규입사 배분은 정기 취합 분기와 독립적으로 처리한다.
        # 수기 입력한 분기는 저장/분류용 기준일 뿐, quarter_items의
        # 취합/배분 가능 여부나 현재 분기 상태를 검증하지 않는다.
        try:
            items_result = (
                admin_supabase
                .table("items")
                .select(
                    "id, product_code, item_name, cost_price, is_active"
                )
                .in_("product_code", product_codes)
                .execute()
            )

            item_map = {
                row["product_code"]: row
                for row in (items_result.data or [])
                if row.get("product_code")
            }

        except Exception as e:
            st.error("상품코드를 기준으로 상품 정보를 확인하지 못했습니다.")
            st.caption(f"오류: {e}")
            return

        display_rows = []

        for row in pasted_rows:
            product_code = row["product_code"]
            item = item_map.get(product_code)

            if not item:
                display_rows.append({
                    "product_code": product_code,
                    "item_id": None,
                    "item_name": "-",
                    "cost_price": None,
                    "status": "missing",
                    "status_text": "⚠ 상품 미등록"
                })
                continue

            if not item.get("is_active"):
                status = "inactive"
                status_text = "⚠ 상품 비활성"
            else:
                # 신규입사 배분은 정기 분기의 취합/배분 설정과 무관하게
                # 등록된 활성 상품이면 배분 대상으로 사용할 수 있습니다.
                status = "active"
                status_text = "✓ 배분 가능"

            display_rows.append({
                "product_code": product_code,
                "item_id": item["id"],
                "item_name": item.get("item_name") or "-",
                "cost_price": item.get("cost_price"),
                "status": status,
                "status_text": status_text
            })

        warning_rows = [
            row
            for row in display_rows
            if row["status"] != "active"
        ]

        if warning_rows:
            st.warning(
                "배분할 수 없는 상품코드가 포함되어 있습니다. "
                "해당 행은 경고만 표시되고 배분 대상에서는 제외됩니다."
            )

        active_count = sum(
            1
            for row in display_rows
            if row["status"] == "active"
        )

        st.markdown(
            f"**상품코드 {len(display_rows)}개 인식 · 배분 가능 {active_count}종**"
        )

        # --------------------------------------------------
        # 6. 상품 목록 + 인라인 수량
        # --------------------------------------------------
        header1, header2, header3, header4 = st.columns(
            [1.5, 4.5, 1.2, 1.1]
        )

        with header1:
            st.markdown("**상품코드**")
        with header2:
            st.markdown("**상품명**")
        with header3:
            st.markdown("**원가**")
        with header4:
            st.markdown("**수량**")

        st.divider()

        valid_rows = []

        for row in display_rows:
            col1, col2, col3, col4 = st.columns(
                [1.5, 4.5, 1.2, 1.1]
            )

            with col1:
                st.write(row["product_code"])

            with col2:
                st.write(row["item_name"])

            with col3:
                raw_cost = row.get("cost_price")
                try:
                    display_cost = (
                        f"{int(str(raw_cost).replace(',', '')):,}원"
                        if raw_cost not in (None, "")
                        else "-"
                    )
                except Exception:
                    display_cost = str(raw_cost) if raw_cost else "-"
                st.write(display_cost)

            with col4:
                if row["status"] == "active":
                    qty = st.number_input(
                        "수량",
                        min_value=0,
                        step=1,
                        value=int(
                            st.session_state.get(
                                f"new_hire_qty_{target_quarter_id}_{row['product_code']}",
                                0
                            )
                        ),
                        key=(
                            f"new_hire_qty_"
                            f"{target_quarter_id}_"
                            f"{row['product_code']}"
                        ),
                        label_visibility="collapsed"
                    )
                else:
                    st.number_input(
                        "수량",
                        min_value=0,
                        step=1,
                        value=0,
                        disabled=True,
                        key=(
                            f"new_hire_disabled_qty_"
                            f"{target_quarter_id}_"
                            f"{row['product_code']}"
                        ),
                        label_visibility="collapsed"
                    )
                    qty = 0

            if row["status"] == "active":
                valid_rows.append({
                    "item_id": row["item_id"],
                    "product_code": row["product_code"],
                    "item_name": row["item_name"],
                    "quantity": int(qty)
                })

        if warning_rows:
            with st.expander(
                "⚠ 배분할 수 없는 상품코드 확인",
                expanded=True
            ):
                for row in warning_rows:
                    st.write(
                        f"⚠ {row['product_code']} | "
                        f"{row['item_name']} | "
                        f"{row['status_text']}"
                    )

        total_quantity_per_user = sum(
            row["quantity"]
            for row in valid_rows
        )

        st.markdown(
            f"**선택 인원:** {len(selected_users)}명  "
            f"| **1인 배분 합계:** {total_quantity_per_user:,}개  "
            f"| **전체 배분 합계:** "
            f"{total_quantity_per_user * len(selected_users):,}개"
        )

        # --------------------------------------------------
        # 7. 저장
        # --------------------------------------------------
        save_spacer, save_button = st.columns([1, 0.16])
        with save_button:
            with st.container(key="new_hire_save_button"):
                if st.button(
                            "입사배분 저장",
                            type="primary",
                            use_container_width=False,
                            key="new_hire_save_distribution"
                        ):

                    if not distribution_title.strip():
                        st.warning("배분 차수 / 명칭을 입력해주세요.")
                        return

                    if not selected_users:
                        st.warning("배분할 인원을 선택해주세요.")
                        return

                    positive_rows = [
                        row
                        for row in valid_rows
                        if row["quantity"] > 0
                    ]

                    if not positive_rows:
                        st.warning(
                            "수량이 1개 이상인 상품을 최소 1개 입력해주세요."
                        )
                        return

                    try:
                        # --------------------------------------------------
                        # 신규입사 저장은 DB RPC 1회 호출만 수행한다.
                        # Python에서 이력 INSERT와 재고 UPDATE를 각각 호출하면
                        # 중간 실패 시 일부만 저장될 수 있으므로, PostgreSQL
                        # transaction 안에서 두 작업을 함께 처리한다.
                        # --------------------------------------------------
                        pending_batch_key = (
                            "new_hire_pending_batch_id"
                        )

                        batch_id = st.session_state.get(
                            pending_batch_key
                        )

                        if not batch_id:
                            batch_id = str(uuid.uuid4())
                            st.session_state[pending_batch_key] = batch_id

                        rpc_rows = [
                            {
                                "user_id": user["id"],
                                "item_id": row["item_id"],
                                "quantity": int(row["quantity"])
                            }
                            for user in selected_users
                            for row in positive_rows
                        ]

                        with loading_guard(
                            "신규입사 배분 저장 중..."
                        ):

                            rpc_result = (
                                admin_supabase
                                .rpc(
                                    "save_new_hire_distribution",
                                    {
                                        "p_batch_id": batch_id,
                                        "p_quarter_id": target_quarter_id,
                                        "p_distribution_title": distribution_title.strip(),
                                        "p_rows": rpc_rows
                                    }
                                )
                                .execute()
                            )

                        result_data = (
                            rpc_result.data
                            if isinstance(rpc_result.data, dict)
                            else {}
                        )

                        inserted_count = int(
                            result_data.get(
                                "inserted_count",
                                len(rpc_rows)
                            )
                        )

                        total_quantity = int(
                            result_data.get(
                                "total_quantity",
                                total_quantity_per_user
                                * len(selected_users)
                            )
                        )

                        # RPC가 성공했다는 것은 이력 INSERT와
                        # user_inventory 반영이 같은 transaction에서
                        # 모두 성공했다는 뜻이다.
                        st.session_state.pop(
                            pending_batch_key,
                            None
                        )

                        # 신규입사 배분이 추가되었으므로 계층형 배치 목록 캐시를 갱신합니다.
                        get_new_hire_batch_catalog.clear()

                        st.session_state[
                            "new_hire_distribution_result"
                        ] = (
                            f"신규입사 배분이 저장되었습니다. "
                            f"{len(selected_users)}명 / "
                            f"{len(positive_rows)}종 / "
                            f"총 {total_quantity:,}개"
                        )

                        # 성공 후 신규입사 임시 입력 상태를 정리한다.
                        for state_key in list(
                            st.session_state.keys()
                        ):
                            if (
                                state_key.startswith("new_hire_qty_")
                                or state_key.startswith("new_hire_disabled_qty_")
                            ):
                                st.session_state.pop(
                                    state_key,
                                    None
                                )

                        st.session_state.pop(
                            "new_hire_pasted_source",
                            None
                        )
                        st.session_state.pop(
                            "new_hire_pasted_rows",
                            None
                        )
                        st.session_state.pop(
                            "new_hire_pasted_text",
                            None
                        )
                        st.session_state.pop(
                            "new_hire_selected_user_labels",
                            None
                        )
                        st.session_state.pop(
                            "new_hire_distribution_title",
                            None
                        )
                        # 위젯이 이미 생성된 뒤에는
                        # new_hire_distribution_mode를 직접 수정하지 않습니다.
                        # 다음 rerun 시작 시 위젯 생성 전에 안전하게 초기화합니다.
                        st.session_state[
                            "new_hire_reset_mode_before_render"
                        ] = True

                        safe_rerun()

                    except Exception as e:
                        # RPC 실패 시 PostgreSQL transaction 자체가
                        # rollback되므로 Python에서 임의로 일부 데이터를
                        # 삭제/복구하지 않는다. 이것이 오히려 안전하다.
                        st.session_state.pop(
                            "new_hire_pending_batch_id",
                            None
                        )
                        st.error(
                            "신규입사 배분 저장에 실패했습니다. "
                            "저장 과정에서 오류가 발생했으며, "
                            "부분 저장되지 않도록 처리되었습니다."
                        )
                        st.caption(f"오류: {e}")
                    finally:
                        reset_loading_state()

        result_message = st.session_state.get(
            "new_hire_distribution_result"
        )

        if result_message:
            st.success(result_message)
            if st.button(
                "확인",
                type="primary",
                use_container_width=True,
                key="new_hire_result_confirm"
            ):
                st.session_state.pop(
                    "new_hire_distribution_result",
                    None
                )
                safe_rerun()

def save_regular_distribution_transaction(
    order_id,
    quarter_id,
    distribution_order_items,
    registered_users
):
    """일반 배분을 PostgreSQL transaction 1회로 저장합니다.

    신규입사 저장과 동일하게 DB transaction을 사용하며,
    같은 order_item + user 조합이 이미 처리된 경우 재시도 시
    user_inventory를 다시 증가시키지 않는 idempotent 구조를 사용합니다.
    """

    rpc_rows = []

    for user in registered_users:
        for order_item in distribution_order_items:
            quantity = int(
                order_item.get("per_user_quantity") or 0
            )

            if quantity <= 0:
                continue

            rpc_rows.append({
                "user_id": user["id"],
                "item_id": order_item["item_id"],
                "order_item_id": order_item["id"],
                "quantity": quantity
            })

    if not rpc_rows:
        return {
            "inserted_count": 0,
            "total_quantity": 0,
            "completed_order_item_ids": []
        }

    rpc_result = (
        admin_supabase
        .rpc(
            "save_regular_distribution",
            {
                "p_order_id": order_id,
                "p_quarter_id": quarter_id,
                "p_rows": rpc_rows
            }
        )
        .execute()
    )

    result_data = (
        rpc_result.data
        if isinstance(rpc_result.data, dict)
        else {}
    )

    return {
        "inserted_count": int(
            result_data.get(
                "inserted_count",
                0
            )
        ),
        "total_quantity": int(
            result_data.get(
                "total_quantity",
                0
            )
        ),
        "completed_order_item_ids": [
            str(order_item_id)
            for order_item_id in result_data.get(
                "completed_order_item_ids",
                []
            )
        ]
    }


@st.dialog("발주 품목", width="large")
def show_order_items_dialog(
    selected_quarter_id
):

    # st.dialog 제목만 사용하여 모달 내부의 중복 "발주 품목" 헤더를 제거한다.

    # --------------------------------------------------
    # 신규입사 모드 진입점
    # --------------------------------------------------
    # 이전 저장 성공 후 다음 rerun에서만 위젯 키를 초기화합니다.
    # 위젯이 생성되기 전이므로 Streamlit session_state 충돌이 발생하지 않습니다.
    if st.session_state.pop(
        "new_hire_reset_mode_before_render",
        False
    ):
        st.session_state.pop(
            "new_hire_distribution_mode",
            None
        )

    # 체크박스는 기존 발주 데이터 조회보다 먼저 평가한다.
    # 따라서 draft order가 없어도 신규입사 배분은 독립적으로 사용할 수 있다.
    new_hire_mode = st.checkbox(
        "신규입사",
        key="new_hire_distribution_mode"
    )

    if new_hire_mode:
        show_new_hire_distribution_ui(
            selected_quarter_id
        )
        return

    st.divider()

    # --------------------------------------------------
    # 발주 조회
    # --------------------------------------------------
    # 모달 내부의 위젯 클릭마다 전체 함수가 다시 실행되므로
    # 최초 진입 시에만 DB를 조회하고, 이후에는 session_state의
    # 데이터를 사용한다. 모달을 새로 열 때는 호출부에서
    # order_dialog_instance를 증가시켜 최신 DB 데이터를 다시 읽는다.

    dialog_instance = st.session_state.get(
        "order_dialog_instance",
        0
    )

    dialog_data_key = (
        f"{selected_quarter_id}_{dialog_instance}"
    )

    cached_order_data = st.session_state.get(
        "order_dialog_data"
    )

    if (
        not cached_order_data
        or cached_order_data.get("key") != dialog_data_key
    ):

        draft_order_result = (
            admin_supabase
            .table("orders")
            .select(
                "id, quarter_id, distribution_user_count, "
                "status, ordered_at, memo"
            )
            .eq(
                "quarter_id",
                selected_quarter_id
            )
            .eq(
                "status",
                "draft"
            )
            .order(
                "created_at",
                desc=True
            )
            .limit(1)
            .execute()
        )

        if not draft_order_result.data:

            st.info(
                "발주에 추가된 품목이 없습니다."
            )

            return

        draft_order_id = (
            draft_order_result.data[0]["id"]
        )

        order_items_result = (
            admin_supabase
            .table("order_items")
            .select(
                "id, item_id, cost_price, "
                "order_quantity, per_user_quantity, memo, "
                "received_at, distributed_at, "
                "items(store_name, product_code, item_name, category_id)"
            )
            .eq(
                "order_id",
                draft_order_id
            )
            .execute()
        )

        st.session_state["order_dialog_data"] = {
            "key": dialog_data_key,
            "draft_order_id": draft_order_id,
            "order_items": order_items_result.data or []
        }

        cached_order_data = (
            st.session_state["order_dialog_data"]
        )

    draft_order_id = cached_order_data[
        "draft_order_id"
    ]

    order_items_data = cached_order_data[
        "order_items"
    ]

    if not order_items_data:

        st.info(
            "발주에 추가된 품목이 없습니다."
        )

        return

    registered_users = (
        get_registered_users()
    )

    registered_user_count = len(
        registered_users
    )

    active_user_count = (
        registered_user_count
    )

    st.markdown(
        f'<div class="order-items-modal-collector-count">취합 인원: {registered_user_count}명</div>',
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # 결과창 닫기
    # --------------------------------------------------

    def close_order_dialog_result():

        st.session_state.pop(
            "order_dialog_result_message",
            None
        )

        st.session_state.pop(
            "order_dialog_result_type",
            None
        )

    # --------------------------------------------------
    # 결과창 표시 함수
    # --------------------------------------------------

    def render_order_dialog_result():

        result_message = (
            st.session_state.get(
                "order_dialog_result_message"
            )
        )

        if not result_message:

            return False

        result_type = (
            st.session_state.get(
                "order_dialog_result_type",
                "info"
            )
        )

        with st.container(
            border=True
        ):

            if result_type == "success":

                st.success(
                    result_message
                )

            elif result_type == "warning":

                st.warning(
                    result_message
                )

            else:

                st.info(
                    result_message
                )

            st.button(
                "확인",
                type="primary",
                use_container_width=True,
                key="order_dialog_result_confirm",
                on_click=(
                    close_order_dialog_result
                )
            )

        return True

    # --------------------------------------------------
    # 발주 품목 모달 전용 스타일
    # --------------------------------------------------

    st.markdown(
        """
        <style>
        /* 이 스타일은 발주 품목 모달에서 사용하는 고유 클래스에만 적용 */
        .order-items-modal-collector-count,
        .order-items-modal-header {
            font-weight: 700 !important;
        }

        .order-items-modal-product-name {
            white-space: normal !important;
            word-break: break-all !important;
            overflow-wrap: anywhere !important;
            line-height: 1.45 !important;
            width: 100% !important;
            box-sizing: border-box !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    # --------------------------------------------------
    # 발주 품목 헤더
    # --------------------------------------------------

    header_col0, header_col1, header_col2, header_col3, header_col4, header_col5, header_col6 = st.columns(
        [2, 2, 3, 2, 2, 2, 3]
    )

    with header_col0:

        st.markdown(
            '<div class="order-items-modal-header">발주 매장</div>',
            unsafe_allow_html=True
        )

    with header_col1:

        st.markdown(
            '<div class="order-items-modal-header">상품코드</div>',
            unsafe_allow_html=True
        )

    with header_col2:

        st.markdown(
            '<div class="order-items-modal-header">상품명</div>',
            unsafe_allow_html=True
        )

    with header_col3:

        st.markdown(
            '<div class="order-items-modal-header">원가</div>',
            unsafe_allow_html=True
        )

    with header_col4:

        st.markdown(
            '<div class="order-items-modal-header">발주수량</div>',
            unsafe_allow_html=True
        )

    with header_col5:

        st.markdown(
            '<div class="order-items-modal-header">1인당 배분수량</div>',
            unsafe_allow_html=True
        )

    with header_col6:

        st.markdown(
            '<div class="order-items-modal-header">메모</div>',
            unsafe_allow_html=True
        )

    st.divider()

    # --------------------------------------------------
    # 발주 품목
    # --------------------------------------------------

    for order_item in (
        order_items_data
    ):

        item = (
            order_item["items"]
        )

        item_id = (
            order_item["item_id"]
        )

        cost_price = (
            order_item["cost_price"]
            or 0
        )

        current_per_user_quantity = (
            order_item["per_user_quantity"]
            or 0
        )

        current_memo = (
            order_item["memo"]
            or ""
        )

        received_at = (
            order_item.get(
                "received_at"
            )
        )

        col0, col1, col2, col3, col4, col5, col6 = st.columns(
            [2, 2, 3, 2, 2, 2, 3]
        )

        with col0:

            st.write(
                item.get("store_name") or "-"
            )

        with col1:

            st.write(item["product_code"])

        with col2:

            product_name = html.escape(
                str(item.get("item_name") or "-")
            )

            st.markdown(
                f'<div class="order-items-modal-product-name">{product_name}</div>',
                unsafe_allow_html=True
            )

        with col3:

            st.write(f"{cost_price:,}원")

        current_order_quantity = (
            active_user_count
            * current_per_user_quantity
        )

        with col4:

            st.write(f"{current_order_quantity:,}개")

        with col5:

            if received_at:
                st.write(f"{current_per_user_quantity:,}개")
            else:
                st.number_input(
                    "1인당 배분수량",
                    min_value=0,
                    step=1,
                    value=current_per_user_quantity,
                    key=f"per_user_qty_{item_id}",
                    label_visibility="collapsed"
                )

        with col6:

            st.text_input(
                "메모",
                value=current_memo,
                key=f"order_memo_{item_id}",
                disabled=bool(received_at),
                label_visibility="collapsed"
            )
        st.divider()

    # --------------------------------------------------
    # 이미 결과창이 떠 있는 경우
    # --------------------------------------------------

    if render_order_dialog_result():

        return

    # --------------------------------------------------
    # 저장/입고 대상
    # --------------------------------------------------

    selected_order_items = [
        order_item
        for order_item in order_items_data
        if not order_item.get("received_at")
    ]

    # --------------------------------------------------
    # 결과창
    # --------------------------------------------------

    if render_order_dialog_result():

        return

    # --------------------------------------------------
    # 발주 작업 버튼
    # --------------------------------------------------

    button_col1, button_col2, button_col3 = st.columns(3)

    # --------------------------------------------------
    # 발주 내용 저장
    # --------------------------------------------------

    with button_col1:

        if st.button(
            "발주 내용 저장",
            type="primary",
            use_container_width=True,
            key="dialog_save_order_items"
        ):

            if not selected_order_items:
                st.session_state["order_dialog_result_message"] = (
                    "저장할 품목이 없습니다."
                )
                st.session_state["order_dialog_result_type"] = "warning"
            else:
                for order_item in selected_order_items:
                    item_id = order_item["item_id"]
                    per_user_quantity = st.session_state.get(
                        f"per_user_qty_{item_id}",
                        order_item.get("per_user_quantity") or 0
                    )
                    memo = st.session_state.get(
                        f"order_memo_{item_id}",
                        order_item.get("memo") or ""
                    )
                    order_quantity = registered_user_count * per_user_quantity

                    (
                        admin_supabase
                        .table("order_items")
                        .update({
                            "per_user_quantity": per_user_quantity,
                            "order_quantity": order_quantity,
                            "memo": memo
                        })
                        .eq("id", order_item["id"])
                        .execute()
                    )

                    order_item["per_user_quantity"] = per_user_quantity
                    order_item["order_quantity"] = order_quantity
                    order_item["memo"] = memo

                st.session_state["order_dialog_result_message"] = (
                    f"{len(selected_order_items)}개 품목의 발주 내용이 저장되었습니다."
                )
                st.session_state["order_dialog_result_type"] = "success"

    # --------------------------------------------------
    # 입고 확정
    # --------------------------------------------------

    with button_col2:

        if st.button(
            "입고 확정",
            use_container_width=True,
            key="dialog_confirm_received"
        ):

            if not selected_order_items:

                st.session_state[
                    "order_dialog_result_message"
                ] = (
                    "입고 확정할 품목을 선택해주세요."
                )

                st.session_state[
                    "order_dialog_result_type"
                ] = "warning"

            else:

                for order_item in (
                    selected_order_items
                ):

                    (
                        admin_supabase
                        .table("order_items")
                        .update(
                            {
                                "received_at":
                                    "now()"
                            }
                        )
                        .eq(
                            "id",
                            order_item["id"]
                        )
                        .execute()
                    )

                    # DB 재조회 없이 현재 모달 상태만 갱신
                    order_item["received_at"] = True

                st.session_state[
                    "order_dialog_result_message"
                ] = (
                    f"{len(selected_order_items)}개 품목이 "
                    "입고 확정되었습니다."
                )

                st.session_state[
                    "order_dialog_result_type"
                ] = "success"

    # --------------------------------------------------
    # 일괄 배분
    # --------------------------------------------------

    distribution_order_items = [
        order_item
        for order_item in order_items_data
        if (
            order_item.get("received_at")
            and not order_item.get("distributed_at")
            and (order_item.get("per_user_quantity") or 0) > 0
        )
    ]

    with button_col3:

        if st.button(
            "일괄 배분",
            use_container_width=True,
            key="dialog_distribute_all"
        ):

            if not distribution_order_items:

                st.session_state[
                    "order_dialog_result_message"
                ] = (
                    "배분할 품목이 없습니다."
                )

                st.session_state[
                    "order_dialog_result_type"
                ] = "warning"

            else:

                try:

                    with loading_guard(
                        "일반 배분 저장 중..."
                    ):
                        save_result = save_regular_distribution_transaction(
                            draft_order_id,
                            selected_quarter_id,
                            distribution_order_items,
                            registered_users
                        )

                    completed_order_item_ids = set(
                        save_result[
                            "completed_order_item_ids"
                        ]
                    )

                    # transaction이 성공한 경우에만 현재 모달 상태를 갱신합니다.
                    for order_item in distribution_order_items:
                        if str(order_item["id"]) in completed_order_item_ids:
                            order_item["distributed_at"] = True

                    inserted_count = int(
                        save_result[
                            "inserted_count"
                        ]
                    )

                    if inserted_count == 0:
                        result_message = (
                            "이미 처리된 배분입니다. "
                            "중복 저장은 발생하지 않았습니다."
                        )
                    else:
                        result_message = (
                            f"{registered_user_count}명에게 "
                            f"{len(distribution_order_items)}개 품목을 "
                            "배분했습니다."
                        )

                    st.session_state[
                        "order_dialog_result_message"
                    ] = result_message

                    st.session_state[
                        "order_dialog_result_type"
                    ] = "success"

                except Exception as exc:

                    # DB transaction이 실패한 경우 부분 저장이 남았다고 가정하지 않고
                    # 현재 화면도 성공 상태로 변경하지 않습니다.
                    st.session_state[
                        "order_dialog_result_message"
                    ] = (
                        "일반 배분 저장에 실패했습니다. "
                        "DB transaction이 완료되지 않아 화면 상태를 유지합니다. "
                        f"오류: {exc}"
                    )

                    st.session_state[
                        "order_dialog_result_type"
                    ] = "error"

@st.dialog("보유수량 처리 완료")
def show_inventory_action_complete():

    result_message = st.session_state.get(
        "inventory_action_result",
        "보유수량 처리가 완료되었습니다."
    )

    st.success(result_message)

    if st.button(
        "확인",
        type="primary",
        use_container_width=True,
        key="confirm_inventory_action_result"
    ):

        st.session_state.pop(
            "inventory_action_result",
            None
        )

        safe_rerun()


@st.dialog("보유수량 수정")
def show_edit_inventory_dialog(
    inventory_id,
    item_name,
    product_code,
    current_qty
):

    st.markdown(
        f"**{item_name}**",
    )
    st.caption(f"상품코드: {product_code}")

    new_qty = st.number_input(
        "보유수량",
        min_value=1,
        step=1,
        value=int(current_qty),
        key=f"inventory_modal_qty_{inventory_id}"
    )

    save_col, delete_col, cancel_col = st.columns(3)

    with save_col:

        if st.button(
            "저장",
            type="primary",
            use_container_width=True,
            key=f"save_inventory_modal_{inventory_id}"
        ):

            (
                admin_supabase
                .table("user_inventory")
                .update({"current_qty": int(new_qty)})
                .eq("id", inventory_id)
                .execute()
            )

            st.session_state[
                "inventory_action_result"
            ] = "보유수량이 저장되었습니다."

            safe_rerun()

    with delete_col:

        if st.button(
            "삭제",
            use_container_width=True,
            key=f"delete_inventory_modal_{inventory_id}"
        ):

            (
                admin_supabase
                .table("user_inventory")
                .delete()
                .eq("id", inventory_id)
                .execute()
            )

            st.session_state[
                "inventory_action_result"
            ] = "보유수량이 삭제되었습니다."

            safe_rerun()

    with cancel_col:

        if st.button(
            "취소",
            use_container_width=True,
            key=f"cancel_inventory_modal_{inventory_id}"
        ):

            safe_rerun()


@st.dialog("상품 수정")
def show_edit_item_dialog(
    edit_item,
    categories,
    major_categories
):

    edit_item_id = edit_item["id"]

    # 수정 완료 메시지 상태
    edit_result = st.session_state.get(
        "edit_item_result"
    )

    if edit_result:

        st.success(
            edit_result
        )

        if st.button(
            "확인",
            type="primary",
            use_container_width=True,
            key=f"confirm_edit_result_{edit_item_id}"
        ):

            st.session_state.pop(
                "edit_item_result",
                None
            )

            st.session_state.pop(
                "edit_item_id",
                None
            )

            safe_rerun()

        return

    edit_store_name = st.text_input(
        "매장명",
        value=edit_item.get("store_name", ""),
        key=f"edit_store_name_{edit_item_id}"
    )

    edit_product_code = st.text_input(
        "상품코드",
        value=edit_item["product_code"],
        key=f"edit_product_code_{edit_item_id}"
    )

    edit_item_name = st.text_input(
        "상품명",
        value=edit_item["item_name"],
        key=f"edit_item_name_{edit_item_id}"
    )

    edit_cost_price = st.text_input(
        "원가 (원)",
        value=(
            str(edit_item["cost_price"])
            if edit_item["cost_price"] is not None
            else ""
        ),
        key=f"edit_cost_price_{edit_item_id}"
    )

    # 현재 상품의 카테고리 확인
    current_category = next(
        (
            category
            for category in categories
            if category["id"] == edit_item["category_id"]
        ),
        None
    )

    # 현재 상품의 대분류 찾기
    if current_category:

        if current_category["parent_id"] is None:
            current_major_id = current_category["id"]

        else:
            current_major_id = current_category["parent_id"]

    else:

        current_major_id = major_categories[0]["id"]

    edit_major_category_options = {
        category["category_name"]: category["id"]
        for category in major_categories
    }

    current_major_name = next(
        (
            category["category_name"]
            for category in major_categories
            if category["id"] == current_major_id
        ),
        list(
            edit_major_category_options.keys()
        )[0]
    )

    edit_major_name = st.selectbox(
        "대분류",
        list(edit_major_category_options.keys()),
        index=list(
            edit_major_category_options.keys()
        ).index(current_major_name),
        key=f"edit_major_category_{edit_item_id}"
    )

    edit_major_id = edit_major_category_options[
        edit_major_name
    ]

    # 선택한 대분류의 소분류 찾기
    edit_sub_categories = [
        category
        for category in categories
        if category["parent_id"] == edit_major_id
    ]

    if edit_sub_categories:

        edit_sub_category_options = {
            category["category_name"]: category["id"]
            for category in edit_sub_categories
        }

        current_edit_sub_id = (
            edit_item["category_id"]
            if (
                current_category
                and current_category["parent_id"] == edit_major_id
            )
            else edit_sub_categories[0]["id"]
        )

        current_edit_sub_name = next(
            (
                category["category_name"]
                for category in edit_sub_categories
                if category["id"] == current_edit_sub_id
            ),
            list(
                edit_sub_category_options.keys()
            )[0]
        )

        edit_sub_name = st.selectbox(
            "소분류",
            list(edit_sub_category_options.keys()),
            index=list(
                edit_sub_category_options.keys()
            ).index(current_edit_sub_name),
            key=f"edit_sub_category_{edit_item_id}"
        )

        selected_edit_category_id = (
            edit_sub_category_options[edit_sub_name]
        )

    else:

        selected_edit_category_id = edit_major_id

    # 취급 상태
    current_status = edit_item["is_active"]

    new_status = st.radio(
        "취급 상태",
        ["IN", "OUT"],
        index=0 if current_status else 1,
        horizontal=True,
        key=f"item_status_{edit_item_id}"
    )

    st.divider()

    # 삭제 확인 상태
    confirm_delete = (
        st.session_state.get(
            "confirm_delete_item_id"
        ) == edit_item_id
    )

    if confirm_delete:

        st.warning(
            f"'{edit_item['item_name']}' 상품을 삭제하시겠습니까?"
        )

        delete_col1, delete_col2 = st.columns(2)

        with delete_col1:

            if st.button(
                "삭제",
                type="primary",
                use_container_width=True,
                key=f"confirm_edit_item_delete_{edit_item_id}"
            ):

                try:

                    admin_supabase.table(
                        "items"
                    ).update(
                        {
                            "is_active": False
                        }
                    ).eq(
                        "id",
                        edit_item_id
                    ).execute()

                    st.session_state.pop(
                        "confirm_delete_item_id",
                        None
                    )

                    st.session_state.pop(
                        "edit_item_id",
                        None
                    )

                    safe_rerun()

                except Exception:

                    st.error(
                        "상품 삭제에 실패했습니다."
                    )

        with delete_col2:

            if st.button(
                "취소",
                use_container_width=True,
                key=f"cancel_edit_item_delete_{edit_item_id}"
            ):

                st.session_state.pop(
                    "confirm_delete_item_id",
                    None
                )

                safe_rerun()

    else:

        edit_col1, edit_col2 = st.columns(2)

        with edit_col1:

            if st.button(
                "수정 저장",
                type="primary",
                use_container_width=True,
                key=f"save_item_edit_{edit_item_id}"
            ):

                if (
                    not edit_store_name
                    or not edit_product_code
                    or not edit_item_name
                    or not edit_cost_price
                ):

                    st.error(
                        "상품코드, 상품명, 원가를 모두 입력해주세요."
                    )

                else:

                    try:

                        edit_cost = int(
                            edit_cost_price
                            .replace(",", "")
                            .strip()
                        )

                        admin_supabase.table(
                            "items"
                        ).update(
                            {
                                "store_name":
                                    edit_store_name,
                                "product_code":
                                    edit_product_code,
                                "item_name":
                                    edit_item_name,
                                "cost_price":
                                    edit_cost,
                                "category_id":
                                    selected_edit_category_id,
                                "is_active":
                                    new_status == "IN"
                            }
                        ).eq(
                            "id",
                            edit_item_id
                        ).execute()

                        st.session_state.pop(
                            "edit_item_id",
                            None
                        )

                        safe_rerun()

                    except Exception as e:

                        st.error(
                            "상품 수정 실패"
                        )

                        st.write(e)

        with edit_col2:

            if st.button(
                "삭제",
                use_container_width=True,
                key=f"delete_from_edit_item_{edit_item_id}"
            ):

                st.session_state[
                    "confirm_delete_item_id"
                ] = edit_item_id

                safe_rerun()

# 처음 진입 화면
if st.session_state.login_mode is None:

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] .main .block-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        [data-testid="stTextInput"] label p {
            font-size: 28px !important;
            font-weight: 700 !important;
        }

        [data-testid="stTextInput"] input {
            font-size: 28px !important;
        }

        /* 로그인 화면 전용 버튼 스타일 */
        .st-key-main_login button {
            background: #2e8b57 !important;
            background-color: #2e8b57 !important;
            border-color: #2e8b57 !important;
            color: #ffffff !important;
        }

        .st-key-main_login button:hover,
        .st-key-main_login button:focus,
        .st-key-main_login button:active {
            background: #26734a !important;
            background-color: #26734a !important;
            border-color: #26734a !important;
            color: #ffffff !important;
        }

        .st-key-main_login button p,
        .st-key-main_login button span {
            color: #ffffff !important;
        }

        .st-key-admin_login_button {
            width: fit-content !important;
            min-width: 0 !important;
            margin-left: auto !important;
            margin-right: 0 !important;
        }

        .st-key-admin_login_button button {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #4a4a4a !important;
            padding: 0 !important;
            min-height: 0 !important;
            height: auto !important;
            font-size: 14px !important;
            font-weight: 400 !important;
            text-decoration: none !important;
            width: fit-content !important;
            min-width: 0 !important;
        }

        .st-key-admin_login_button button:hover,
        .st-key-admin_login_button button:focus,
        .st-key-admin_login_button button:active {
            background: transparent !important;
            background-color: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: #2e8b57 !important;
        }

        .st-key-admin_login_button button p,
        .st-key-admin_login_button button span {
            color: #4a4a4a !important;
        }

        .st-key-admin_login_button button:hover p,
        .st-key-admin_login_button button:hover span {
            color: #2e8b57 !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    _, login_form_col, _ = st.columns(
        [1, 0.4, 1]
    )

    with login_form_col:

        employee_no = st.text_input(
            "사번",
            key="login_employee_no"
        )

        user_name = st.text_input(
            "이름",
            key="login_user_name"
        )

        login_col, admin_col = st.columns(2)

        with login_col:

            if st.button(
                "LOG IN",
                type="primary",
                key="main_login"
            ):

                if not employee_no or not user_name:

                    st.error(
                        "사번과 이름을 모두 입력해주세요."
                    )

                else:

                    try:
                        with loading_guard("로그인 확인 중..."):
                            user_result = (
                                admin_supabase
                                .table("users")
                                .select(
                                    "id, name, employee_no, "
                                    "is_active, role"
                                )
                                .eq(
                                    "employee_no",
                                    employee_no
                                )
                                .eq(
                                    "name",
                                    user_name
                                )
                                .eq(
                                    "is_active",
                                    True
                                )
                                .limit(1)
                                .execute()
                            )
                    except Exception as e:
                        st.error("로그인 확인 중 오류가 발생했습니다.")
                        st.write(e)
                    else:
                        if not user_result.data:
                            st.error(
                                "등록된 사용자 정보를 찾을 수 없습니다."
                            )
                        else:
                            identified_user = user_result.data[0]

                            st.session_state.login_mode = "user"
                            st.session_state.user_notice_dismissed = False
                            st.session_state.show_user_collection = True
                            st.session_state.collection_user_id = (
                                identified_user["id"]
                            )
                            st.session_state.collection_identified_name = (
                                identified_user["name"]
                            )

                            # rerun은 loading_guard 바깥에서 실행합니다.
                            safe_rerun()


        with admin_col:

            if st.button(
                "관리자",
                key="admin_login_button"
            ):

                st.session_state.login_mode = "admin"
                st.session_state.admin_login = True

                safe_rerun()

    st.stop()

# 관리자 로그인
if (
    st.session_state.login_mode == "admin"
    and not st.session_state.logged_in
):

    st.markdown(
        """
        <style>
        [data-testid="stAppViewContainer"] .main .block-container {
            min-height: 100vh;
            display: flex;
            flex-direction: column;
            justify-content: center;
        }

        [data-testid="stTextInput"] label p {
            font-size: 28px !important;
            font-weight: 700 !important;
        }

        [data-testid="stTextInput"] input {
            font-size: 28px !important;
        }

        /* 관리자 로그인 화면 전용 헤더/로그인 버튼 스타일 */
        h3 {
            color: #2e8b57 !important;
        }

        .st-key-admin_login_submit button {
            background: #2e8b57 !important;
            background-color: #2e8b57 !important;
            border-color: #2e8b57 !important;
            color: #ffffff !important;
        }

        .st-key-admin_login_submit button:hover,
        .st-key-admin_login_submit button:focus,
        .st-key-admin_login_submit button:active {
            background: #26734a !important;
            background-color: #26734a !important;
            border-color: #26734a !important;
            color: #ffffff !important;
        }

        .st-key-admin_login_submit button p,
        .st-key-admin_login_submit button span {
            color: #ffffff !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    _, login_form_col, _ = st.columns(
        [1, 0.4, 1]
    )

    with login_form_col:

        st.subheader("관리자 로그인")

        email = st.text_input(
            "이메일",
            key="admin_email"
        )

        password = st.text_input(
            "비밀번호",
            type="password",
            key="admin_password"
        )

        if st.button(
            "로그인",
            type="primary",
            key="admin_login_submit"
        ):

            if not email or not password:
                st.error("이메일과 비밀번호를 입력해주세요.")

            else:

                try:
                    with loading_guard("관리자 로그인 확인 중..."):
                        result = supabase.auth.sign_in_with_password({
                            "email": email,
                            "password": password
                        })

                        if not result.user or not result.session:
                            result = None
                            admin_check = None
                        else:
                            user_id = result.user.id

                            admin_check = (
                                admin_supabase
                                .table("users")
                                .select(
                                    "name, employee_no, role"
                                )
                                .eq(
                                    "auth_user_id",
                                    user_id
                                )
                                .single()
                                .execute()
                            )

                except Exception as e:
                    st.error("로그인 실패")
                    st.write(str(e))

                else:
                    if result is None:
                        st.error("로그인 정보를 확인할 수 없습니다.")
                    else:
                        user_info = admin_check.data if admin_check else None

                        if not user_info:
                            st.error(
                                "관리자 사용자 정보가 등록되어 있지 않습니다."
                            )

                        elif user_info["role"] != "admin":
                            st.error(
                                "관리자 권한이 없습니다."
                            )

                        else:
                            st.session_state.logged_in = True
                            st.session_state.auth_access_token = (
                                result.session.access_token
                            )
                            st.session_state.auth_refresh_token = (
                                result.session.refresh_token
                            )
                            st.session_state.admin_user = user_info

                            st.success("관리자 로그인 성공!")

                            # rerun은 loading_guard 바깥에서 실행합니다.
                            safe_rerun()

    st.stop()

menu = None

if st.session_state.logged_in:

    if st.button(
        "로그아웃",
        key="admin_logout",
        type="tertiary",
        width="content"
    ):
        st.session_state.logged_in = False
        st.session_state.login_mode = None
        st.session_state.admin_login = False
        st.session_state.show_user_collection = False
        st.session_state.collection_user_id = None
        st.session_state.collection_identified_name = None
        st.session_state.admin_user = None
        st.session_state.auth_access_token = None
        st.session_state.auth_refresh_token = None
        safe_rerun()

    st.markdown(
        """
        <style>
        /* 관리자 페이지 전체 고정 레이아웃 */
        html,
        body {
            min-width: 1600px !important;
            overflow-x: auto !important;
        }

        [data-testid="stAppViewContainer"] {
            min-width: 1600px !important;
        }

        [data-testid="stAppViewContainer"] .main .block-container {
            width: 1600px !important;
            min-width: 1600px !important;
            max-width: 1600px !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
        }

        [data-testid="stColumn"] {
            min-width: 0 !important;
        }

        [data-testid="stColumn"] button,
        [data-testid="stColumn"] p,
        [data-testid="stColumn"] span,
        [data-testid="stColumn"] label {
            white-space: nowrap !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    admin_menu_area, admin_content_area = st.columns(
        [1, 8],
        gap="large"
    )

    with admin_menu_area:

        st.markdown(
            """
            <div style="
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 12px;
            ">
                관리자 메뉴
            </div>
            """,
            unsafe_allow_html=True
        )

        st.markdown(
            """
            <style>
            div[data-testid="stColumn"]:has(
                button[key^="admin_menu_"]
            ) button {
                background: transparent !important;
                border: none !important;
                box-shadow: none !important;
                color: inherit !important;
                justify-content: flex-start !important;
                padding-left: 0 !important;
                font-size: 20px !important;
                font-weight: 400 !important;
                white-space: nowrap !important;
            }

            div[data-testid="stColumn"]:has(
                button[key^="admin_menu_"]
            ) button:hover {
                color: #ff4b4b !important;
            }

            div[data-testid="stColumn"]:has(
                button[key^="admin_menu_"]
            ) {
                margin-left: 0 !important;
            }
            </style>
            """,
            unsafe_allow_html=True
        )

        admin_menu_items = [
            ("대시보드", "admin_menu_dashboard"),
            ("인원 관리", "admin_menu_users"),
            ("품목 관리", "admin_menu_items"),
            ("분기/취합 관리", "admin_menu_quarter"),
            ("발주/배분 관리", "admin_menu_orders"),
            ("폐기 관리", "admin_menu_disposal"),
            ("보유수량 조회", "admin_menu_inventory"),
            ("처리내역", "admin_menu_history"),
        ]

        if "admin_menu" not in st.session_state:
            st.session_state.admin_menu = "대시보드"

        if st.session_state.get("admin_menu") == "발주 관리":
            st.session_state.admin_menu = "발주/배분 관리"

        for menu_name, menu_key in admin_menu_items:

            if st.button(
                menu_name,
                key=menu_key,
                type="tertiary",
                width="content"
            ):

                previous_menu = st.session_state.get("admin_menu")
                st.session_state.admin_menu = menu_name

                # 보유수량 조회 -> 처리내역 전환 시 이전 화면의 위젯 상태를 선제적으로 정리
                #하여 프런트엔드에 이전 행 컴포넌트가 남아 보이는 현상을 방어합니다.
                if (
                    previous_menu == "보유수량 조회"
                    and menu_name == "처리내역"
                ):
                    for state_key in list(st.session_state.keys()):
                        if state_key.startswith("inventory_row_"):
                            st.session_state.pop(state_key, None)
                    st.session_state.pop("inventory_action_result", None)

                reset_menu_transition_state()

    menu = st.session_state.admin_menu

    # 메뉴 버튼 클릭 시 이미 임시 상태를 정리했으므로,
    # 렌더링 직전에 동일한 cleanup을 한 번 더 수행하지 않습니다.
    st.session_state.previous_admin_menu = menu


    with admin_content_area:

        if menu == "대시보드":

            current_quarter = get_current_quarter()

            # --------------------------------------------------
            # 현재 취합 분기 안내
            # --------------------------------------------------

            if current_quarter:

                st.markdown(
                    f"### {current_quarter['year']}년 "
                    f"{current_quarter['quarter']}분기 취합"
                )

                st.caption(
                    f"취합 기간: "
                    f"{current_quarter['start_date']} ~ "
                    f"{current_quarter['end_date']}"
                )

            else:

                st.markdown("### 현재 취합 기간이 아닙니다.")

                st.caption(
                    "현재 진행 중인 취합 분기가 없습니다."
                )

            # --------------------------------------------------
            # 기본 데이터 조회
            # --------------------------------------------------

            active_users = get_registered_users()

            active_user_count = len(
                active_users
            )

            request_user_ids = []

            if current_quarter:

                request_result = (
                    admin_supabase
                    .table("requests")
                    .select("user_id")
                    .eq(
                        "quarter_id",
                        current_quarter["id"]
                    )
                    .execute()
                )

                request_user_ids = list(
                    set(
                        row["user_id"]
                        for row in request_result.data
                    )
                )

            collected_user_count = len(
                request_user_ids
            )

            not_collected_user_count = max(
                active_user_count - collected_user_count,
                0
            )

            # 발주 / 입고
            order_item_count = 0
            received_item_count = 0
            waiting_receive_item_count = 0
            order_items_result = None

            if current_quarter:

                order_result = (
                    admin_supabase
                    .table("orders")
                    .select("id")
                    .eq(
                        "quarter_id",
                        current_quarter["id"]
                    )
                    .order(
                        "created_at",
                        desc=True
                    )
                    .limit(1)
                    .execute()
                )

                if order_result.data:

                    current_order_id = order_result.data[0]["id"]

                    order_items_result = (
                        admin_supabase
                        .table("order_items")
                        .select(
                            "id, received_at, distributed_at"
                        )
                        .eq(
                            "order_id",
                            current_order_id
                        )
                        .execute()
                    )

                    order_item_count = len(
                        order_items_result.data
                    )

                    received_item_count = sum(
                        1
                        for item in order_items_result.data
                        if item["received_at"] is not None
                    )

                    waiting_receive_item_count = (
                        order_item_count
                        - received_item_count
                    )

            # 배분
            distributed_item_count = 0
            waiting_distribution_item_count = 0

            if (
                current_quarter
                and order_items_result
            ):

                distributed_item_count = sum(
                    1
                    for item in order_items_result.data
                    if item["distributed_at"] is not None
                )

                waiting_distribution_item_count = (
                    order_item_count
                    - distributed_item_count
                )

            # 폐기
            disposal_request_count = 0
            disposal_approved_count = 0
            disposal_pending_count = 0

            if current_quarter:

                disposal_result = (
                    admin_supabase
                    .table("disposals")
                    .select("id, status")
                    .eq(
                        "quarter_id",
                        current_quarter["id"]
                    )
                    .execute()
                )

                disposal_request_count = len(
                    disposal_result.data
                )

                disposal_approved_count = sum(
                    1
                    for disposal in disposal_result.data
                    if disposal["status"] == "approved"
                )

                disposal_pending_count = (
                    disposal_request_count
                    - disposal_approved_count
                )

            # --------------------------------------------------
            # 대시보드 레이아웃
            # 왼쪽: 취합 현황 + 취합 대상
            # 오른쪽: 나머지 4개 현황을 2 x 2로 배치
            # --------------------------------------------------

            dashboard_left, dashboard_right = st.columns(
                [1, 2],
                gap="large"
            )

            with dashboard_left:

                st.markdown(
                    """
                    <style>
                    .dashboard-progress {
                        width: 80%;
                        height: 28px;
                        background: #eef1f4;
                        border-radius: 14px;
                        overflow: hidden;
                        position: relative;
                        margin-top: 8px;
                        margin-bottom: 6px;
                    }

                    .dashboard-progress-bar {
                        height: 100%;
                        background: #22a447;
                        border-radius: 14px;
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        color: white;
                        font-size: 15px;
                        font-weight: 700;
                        min-width: 0;
                    }

                    .dashboard-target-label {
                        font-size: 18px;
                        font-weight: 600;
                        margin-top: 16px;
                        margin-bottom: 2px;
                    }

                    .dashboard-target-value {
                        font-size: 32px;
                        line-height: 1.15;
                        margin-bottom: 12px;
                    }

                    .dashboard-collection-label {
                        font-size: 18px;
                        font-weight: 600;
                        margin-bottom: 0;
                    }

                    .dashboard-collection-button button {
                        font-size: 32px !important;
                        font-weight: 600 !important;
                        min-height: 38px !important;
                        height: 38px !important;
                        padding-top: 0 !important;
                        padding-bottom: 0 !important;
                        margin-top: -4px !important;
                    }

                    .dashboard-circle-grid {
                        display: flex;
                        margin-top: 18px;
                    }

                    .dashboard-circle-item {
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                    }

                    .dashboard-circle {
                        width: 156px;
                        height: 156px;
                        border-radius: 50%;
                        border: 8px solid #e8edf2;
                        display: flex;
                        flex-direction: column;
                        align-items: center;
                        justify-content: center;
                        box-sizing: border-box;
                        background: linear-gradient(145deg, #ffffff, #f6f8fa);
                        box-shadow: 0 8px 20px rgba(15, 23, 42, 0.08);
                        position: relative;
                    }

                    .dashboard-circle::before {
                        content: '';
                        position: absolute;
                        inset: 7px;
                        border-radius: 50%;
                        border: 1px dashed #d8dee5;
                        pointer-events: none;
                    }

                    .dashboard-circle-dual {
                        display: flex;
                        align-items: center;
                        justify-content: center;
                        gap: 16px;
                        position: relative;
                        z-index: 1;
                    }

                    .dashboard-circle-stat {
                        min-width: 48px;
                        text-align: center;
                    }

                    .dashboard-circle-stat-label {
                        font-size: 12px;
                        font-weight: 600;
                        color: #68707a;
                        margin-bottom: 5px;
                    }

                    .dashboard-circle-stat-value {
                        font-size: 27px;
                        font-weight: 800;
                        line-height: 1;
                    }

                    .dashboard-circle-divider {
                        width: 1px;
                        height: 48px;
                        background: #dfe4e9;
                    }

                    .dashboard-circle-triple {
                        width: 118px;
                        height: 118px;
                        border-radius: 50%;
                        position: relative;
                        z-index: 1;
                        background: conic-gradient(
                            from -90deg,
                            #fff1f2 0deg 116deg,
                            #ffffff 116deg 120deg,
                            #ffe4e6 120deg 236deg,
                            #ffffff 236deg 240deg,
                            #fecdd3 240deg 356deg,
                            #ffffff 356deg 360deg
                        );
                        box-shadow: inset 0 0 0 1px rgba(255,255,255,0.9);
                    }

                    .dashboard-circle-triple-stat {
                        position: absolute;
                        width: 42px;
                        text-align: center;
                        line-height: 1;
                        z-index: 2;
                    }

                    .dashboard-circle-triple-stat-label {
                        font-size: 9px;
                        font-weight: 600;
                        color: #68707a;
                        margin-bottom: 4px;
                        white-space: nowrap;
                    }

                    .dashboard-circle-triple-stat-value {
                        font-size: 23px;
                        font-weight: 800;
                        color: #20242a;
                    }

                    .dashboard-circle-triple-stat-top {
                        top: 17px;
                        left: 50%;
                        transform: translateX(-50%);
                    }

                    .dashboard-circle-triple-stat-left {
                        left: 4px;
                        bottom: 17px;
                    }

                    .dashboard-circle-triple-stat-right {
                        right: 4px;
                        bottom: 17px;
                    }

                    .dashboard-circle-triple-ray {
                        position: absolute;
                        left: 50%;
                        top: 50%;
                        width: 1px;
                        height: 52px;
                        background: rgba(174, 88, 100, 0.25);
                        transform-origin: 50% 0;
                    }

                    .dashboard-circle-triple-ray-a {
                        transform: translate(-50%, 0) rotate(0deg);
                    }

                    .dashboard-circle-triple-ray-b {
                        transform: translate(-50%, 0) rotate(120deg);
                    }

                    .dashboard-circle-triple-ray-c {
                        transform: translate(-50%, 0) rotate(240deg);
                    }

                    .dashboard-circle-label {
                        font-size: 14px;
                        font-weight: 700;
                        margin-top: 9px;
                        color: #333;
                    }

                    .dashboard-attention-list {
                        display: flex;
                        flex-direction: column;
                        gap: 10px;
                        margin-top: 18px;
                    }

                    .dashboard-attention-item {
                        padding: 13px 15px;
                        border-radius: 10px;
                        font-size: 14px;
                        font-weight: 700;
                        background: #fff;
                        box-shadow: 0 4px 14px rgba(15, 23, 42, 0.06);
                    }

                    .dashboard-attention-warning {
                        border: 1px solid #fed7aa;
                        border-left: 5px solid #f59e0b;
                        background: #fffaf2;
                    }

                    .dashboard-attention-danger {
                        border: 1px solid #fecaca;
                        border-left: 5px solid #ef4444;
                        background: #fff5f5;
                    }

                    .dashboard-attention-info {
                        border: 1px solid #bfdbfe;
                        border-left: 5px solid #3b82f6;
                        background: #f5f9ff;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                st.markdown("#### 취합 현황")

                if current_quarter:

                    # 취합 대상 정보를 취합 현황 헤더 바로 아래로 이동
                    st.markdown(
                        "<div class='dashboard-target-label'>대상 인원</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        f"<div class='dashboard-target-value'>{active_user_count}명</div>",
                        unsafe_allow_html=True
                    )

                    if active_user_count > 0:
                        collection_rate = round(
                            collected_user_count
                            / active_user_count
                            * 100
                        )
                    else:
                        collection_rate = 0

                    progress_width = min(100, max(0, collection_rate))

                    st.markdown(
                        f"""
                        <div class="dashboard-progress">
                            <div
                                class="dashboard-progress-bar"
                                style="width: {progress_width}%;"
                            >
                                {collection_rate}%
                            </div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )

                    st.markdown("<br>", unsafe_allow_html=True)

                    # 완료 / 미취합을 왼쪽에 붙여 좁은 영역으로 배치
                    collection_col1, collection_col2, collection_spacer = st.columns(
                        [1, 1, 3],
                        gap="small"
                    )

                    with collection_col1:

                        st.markdown(
                            "<div class='dashboard-collection-label'>완료</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            "<div class='dashboard-collection-button'>",
                            unsafe_allow_html=True
                        )

                        if st.button(
                            f"{collected_user_count}명",
                            key="dashboard_collected_users",
                            width="content",
                            type="tertiary"
                        ):
                            st.session_state[
                                "dashboard_collection_detail"
                            ] = "완료"

                        st.markdown("</div>", unsafe_allow_html=True)

                    with collection_col2:

                        st.markdown(
                            "<div class='dashboard-collection-label'>미취합</div>",
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            "<div class='dashboard-collection-button'>",
                            unsafe_allow_html=True
                        )

                        if st.button(
                            f"{not_collected_user_count}명",
                            key="dashboard_not_collected_users",
                            width="content",
                            type="tertiary"
                        ):
                            st.session_state[
                                "dashboard_collection_detail"
                            ] = "미취합"

                        st.markdown("</div>", unsafe_allow_html=True)

                    detail_type = st.session_state.get(
                        "dashboard_collection_detail"
                    )

                    if detail_type == "완료":

                        completed_users = [
                            user
                            for user in active_users
                            if user["id"] in request_user_ids
                        ]

                        st.caption("취합 완료 인원")

                        if completed_users:
                            for user in completed_users:
                                st.write(
                                    f"• {user['name']} ({user['employee_no']})"
                                )
                        else:
                            st.caption("해당 인원이 없습니다.")

                    elif detail_type == "미취합":

                        not_collected_users = [
                            user
                            for user in active_users
                            if user["id"] not in request_user_ids
                        ]

                        st.caption("미취합 인원")

                        if not_collected_users:
                            for user in not_collected_users:
                                st.write(
                                    f"• {user['name']} ({user['employee_no']})"
                                )
                        else:
                            st.caption("해당 인원이 없습니다.")

                else:

                    st.markdown(
                        "<div class='dashboard-target-label'>상태</div>",
                        unsafe_allow_html=True
                    )
                    st.markdown(
                        "<div class='dashboard-target-value'>-</div>",
                        unsafe_allow_html=True
                    )

            with dashboard_right:

                dashboard_col1, dashboard_col2, dashboard_col3 = st.columns(3)

                with dashboard_col1:

                    st.markdown("#### 발주 / 입고")

                    if current_quarter:
                        st.markdown(
                            f"""
                            <div class="dashboard-circle-grid">
                                <div class="dashboard-circle-item">
                                    <div class="dashboard-circle" style="border-color:#bfdbfe;">
                                        <div class="dashboard-circle-dual">
                                            <div class="dashboard-circle-stat">
                                                <div class="dashboard-circle-stat-label">발주</div>
                                                <div class="dashboard-circle-stat-value">{order_item_count}</div>
                                            </div>
                                            <div class="dashboard-circle-divider"></div>
                                            <div class="dashboard-circle-stat">
                                                <div class="dashboard-circle-stat-label">입고</div>
                                                <div class="dashboard-circle-stat-value">{received_item_count}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                        if waiting_receive_item_count > 0:
                            st.caption(
                                f"입고 대기 {waiting_receive_item_count}종"
                            )
                    else:
                        st.caption("상태 -")

                with dashboard_col2:

                    st.markdown("#### 배분 현황")

                    if current_quarter:
                        st.markdown(
                            f"""
                            <div class="dashboard-circle-grid">
                                <div class="dashboard-circle-item">
                                    <div class="dashboard-circle" style="border-color:#bbf7d0;">
                                        <div class="dashboard-circle-dual">
                                            <div class="dashboard-circle-stat">
                                                <div class="dashboard-circle-stat-label">완료</div>
                                                <div class="dashboard-circle-stat-value">{distributed_item_count}</div>
                                            </div>
                                            <div class="dashboard-circle-divider"></div>
                                            <div class="dashboard-circle-stat">
                                                <div class="dashboard-circle-stat-label">대기</div>
                                                <div class="dashboard-circle-stat-value">{waiting_distribution_item_count}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )
                    else:
                        st.caption("상태 -")

                with dashboard_col3:

                    st.markdown("#### 폐기 현황")

                    if current_quarter:
                        st.markdown(
                            f"""
                            <div class="dashboard-circle-grid">
                                <div class="dashboard-circle-item">
                                    <div class="dashboard-circle" style="border-color:#fecaca;">
                                        <div class="dashboard-circle-dual">
                                            <div class="dashboard-circle-stat">
                                                <div class="dashboard-circle-stat-label">신청</div>
                                                <div class="dashboard-circle-stat-value">{disposal_request_count}</div>
                                            </div>
                                            <div class="dashboard-circle-divider"></div>
                                            <div class="dashboard-circle-stat">
                                                <div class="dashboard-circle-stat-label">확정</div>
                                                <div class="dashboard-circle-stat-value">{disposal_approved_count}</div>
                                            </div>
                                        </div>
                                    </div>
                                </div>
                            </div>
                            """,
                            unsafe_allow_html=True
                        )

                        if disposal_pending_count > 0:
                            st.caption(
                                f"확정 대기 {disposal_pending_count}건"
                            )
                    else:
                        st.caption("상태 -")

                st.markdown("<div style='height: 18px;'></div>", unsafe_allow_html=True)

                with dashboard_col1:

                    st.markdown("#### ⚠️ 확인 필요")

                    attention_items = []

                    if current_quarter:
                        if not_collected_user_count > 0:
                            attention_items.append(
                                (
                                    "warning",
                                    f"미취합 {not_collected_user_count}명"
                                )
                            )
                        if waiting_receive_item_count > 0:
                            attention_items.append(
                                (
                                    "info",
                                    f"입고 대기 {waiting_receive_item_count}종"
                                )
                            )
                        if waiting_distribution_item_count > 0:
                            attention_items.append(
                                (
                                    "warning",
                                    f"배분 대기 {waiting_distribution_item_count}종"
                                )
                            )
                        if disposal_pending_count > 0:
                            attention_items.append(
                                (
                                    "danger",
                                    f"폐기 확정 대기 {disposal_pending_count}건"
                                )
                            )

                    if attention_items:
                        attention_html = [
                            '<div class="dashboard-attention-list">'
                        ]

                        for level, text in attention_items:
                            icon = {
                                "warning": "⚠️",
                                "danger": "🚨",
                                "info": "📦"
                            }.get(level, "•")
                            attention_html.append(
                                f'<div class="dashboard-attention-item dashboard-attention-{level}">{icon}&nbsp;&nbsp;{text}</div>'
                            )

                        attention_html.append('</div>')

                        st.markdown(
                            "".join(attention_html),
                            unsafe_allow_html=True
                        )
                    else:
                        st.markdown(
                            '<div class="dashboard-attention-empty">✓ 현재 확인이 필요한 항목이 없습니다.</div>',
                            unsafe_allow_html=True
                        )


        elif menu == "인원 관리":

            # 화면의 왼쪽 절반만 사용
            left_col, right_col = st.columns([1, 1])

            with left_col:

                users_result = get_registered_users()

                # --------------------------------------------------
                # 인원 목록 제목 + 추가 버튼
                # 테이블 영역과 동일한 부모 범위에서 우측 끝 정렬
                # --------------------------------------------------

                sorted_users = sorted(
                    users_result or [],
                    key=lambda x: x["name"]
                )

                employee_max_len = max(
                    [len("사번")]
                    + [
                        len(str(user.get("employee_no", "")))
                        for user in sorted_users
                    ],
                    default=len("사번")
                )

                name_max_len = max(
                    [len("이름")]
                    + [
                        len(str(user.get("name", "")))
                        for user in sorted_users
                    ],
                    default=len("이름")
                )

                # 데이터 최대 길이에 따라 열 너비 비율 계산
                employee_width = max(
                    72,
                    employee_max_len * 9 + 28
                )
                name_width = max(
                    72,
                    name_max_len * 14 + 28
                )

                with st.container(key="people_header"):

                    st.markdown(
                        f"""
                        <style>
                        /* --------------------------------------------------
                           인원관리 헤더는 테이블과 동일한 2열 그리드 폭 사용
                           - 첫 번째 트랙: 사번 열
                           - 두 번째 트랙: 이름 열
                           - 추가 버튼의 우측 경계 = 이름 열 우측 경계
                           -------------------------------------------------- */
                        .st-key-people_header {{
                            width: 33.333333% !important;
                            max-width: 33.333333% !important;
                            margin-left: 0 !important;
                            margin-right: auto !important;
                            box-sizing: border-box !important;
                            margin-bottom: 0 !important;
                            padding: 0 !important;
                        }}

                        .st-key-people_header [data-testid="stHorizontalBlock"] {{
                            width: 100% !important;
                            max-width: 100% !important;
                            box-sizing: border-box !important;
                            display: grid !important;
                            grid-template-columns: {employee_width}fr {name_width}fr !important;
                            gap: 0 !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }}

                        .st-key-people_header [data-testid="stColumn"] {{
                            min-width: 0 !important;
                            width: auto !important;
                            box-sizing: border-box !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }}

                        .st-key-people_header [data-testid="stColumn"]:last-child {{
                            display: flex !important;
                            justify-content: flex-end !important;
                            align-items: flex-start !important;
                            width: 100% !important;
                            box-sizing: border-box !important;
                        }}

                        .st-key-people_header [class*="st-key-open_add_user"] {{
                            width: 100% !important;
                            max-width: 100% !important;
                            box-sizing: border-box !important;
                            display: flex !important;
                            justify-content: flex-end !important;
                            align-items: flex-start !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }}

                        .st-key-people_header [class*="st-key-open_add_user"] > div {{
                            width: 100% !important;
                            max-width: 100% !important;
                            box-sizing: border-box !important;
                            display: flex !important;
                            justify-content: flex-end !important;
                            align-items: flex-start !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }}

                        .st-key-people_header [class*="st-key-open_add_user"] button {{
                            width: 32px !important;
                            height: 32px !important;
                            min-width: 32px !important;
                            min-height: 32px !important;
                            flex: 0 0 32px !important;
                            padding: 0 !important;
                            margin: 0 !important;
                            border-radius: 50% !important;
                            background: #2e8b57 !important;
                            border: none !important;
                            box-shadow: none !important;
                            color: #ffffff !important;
                            font-size: 20px !important;
                            font-weight: 900 !important;
                            line-height: 1 !important;
                            display: flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            box-sizing: border-box !important;
                        }}

                        .st-key-people_header [class*="st-key-open_add_user"] button p {{
                            color: #ffffff !important;
                            font-size: 20px !important;
                            font-weight: 900 !important;
                            line-height: 1 !important;
                            margin: 0 !important;
                            padding: 0 !important;
                            display: flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            transform: translateY(-1px) !important;
                        }}

                        .st-key-people_header [class*="st-key-open_add_user"] button:hover {{
                            background: #26734a !important;
                            border: none !important;
                        }}

                        .st-key-people_header .people-headcount {{
                            margin: 2px 0 8px !important;
                            padding: 0 !important;
                            font-size: 14px !important;
                            font-weight: 500 !important;
                            line-height: 1.4 !important;
                            color: #495057 !important;
                        }}
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    # 테이블과 동일한 2열 트랙을 직접 지정하여
                    # 추가 버튼의 우측 끝을 이름 열 우측 끝에 고정
                    title_col, btn_col = st.columns(
                        [employee_width, name_width],
                        gap=None
                    )

                    with title_col:
                        st.subheader("인원 목록")

                    st.markdown(
                        f'<div class="people-headcount">총 인원: {len(sorted_users)}명</div>',
                        unsafe_allow_html=True
                    )

                    with btn_col:
                        if st.button(
                            "+",
                            key="open_add_user"
                        ):
                            st.session_state.pop(
                                "edit_user_id",
                                None
                            )
                            st.session_state.pop(
                                "confirm_delete_user_id",
                                None
                            )
                            show_add_user_dialog()

                # --------------------------------------------------
                # 인원 목록 : 최대 데이터 길이에 맞춘 동적 열 너비
                # --------------------------------------------------

                with st.container(key="people_table"):

                    st.markdown(
                        """
                        <style>
                        /* 인원관리 테이블 영역에만 적용 */
                        .st-key-people_table {
                            width: 33.333333% !important;
                            max-width: 33.333333% !important;
                            margin-left: 0 !important;
                            margin-right: auto !important;
                            box-sizing: border-box !important;
                        }

                        .st-key-people_table [data-testid="stVerticalBlock"],
                        .st-key-people_table [data-testid="stElementContainer"],
                        .st-key-people_table [data-testid="element-container"] {
                            gap: 0 !important;
                            margin: 0 !important;
                            padding-top: 0 !important;
                            padding-bottom: 0 !important;
                        }

                        .st-key-people_table [data-testid="stHorizontalBlock"] {
                            gap: 0 !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }

                        .st-key-people_table [data-testid="stColumn"] {
                            min-width: 0 !important;
                            margin: 0 !important;
                            padding-left: 0 !important;
                            padding-right: 0 !important;
                            box-sizing: border-box !important;
                        }

                        .st-key-people_table .people-grid-cell {
                            width: 100%;
                            height: 44px !important;
                            min-height: 44px !important;
                            max-height: 44px !important;
                            box-sizing: border-box;
                            display: flex;
                            align-items: center;
                            justify-content: center !important;
                            padding: 0 10px !important;
                            margin: 0 !important;
                            background: #ffffff;
                            border-top: 1px solid #d9dde2;
                            border-left: 1px solid #d9dde2;
                            border-bottom: 1px solid #d9dde2;
                            font-size: 14px;
                            line-height: 1.2 !important;
                            text-align: center !important;
                            white-space: nowrap;
                            overflow: hidden;
                        }

                        .st-key-people_table .people-grid-cell-last {
                            border-right: 1px solid #d9dde2;
                        }

                        .st-key-people_table .people-grid-header {
                            background: #f7f8fa;
                            font-weight: 700;
                        }

                        .st-key-people_table [class*="st-key-edit_user_"] {
                            width: 100% !important;
                            min-width: 0 !important;
                            height: 44px !important;
                            min-height: 44px !important;
                            margin: 0 !important;
                            padding: 0 !important;
                            box-sizing: border-box !important;
                        }

                        .st-key-people_table [class*="st-key-edit_user_"] button {
                            width: 100% !important;
                            height: 44px !important;
                            min-height: 44px !important;
                            margin: 0 !important;
                            padding: 0 10px !important;
                            border-top: 0 !important;
                            border-left: 1px solid #d9dde2 !important;
                            border-bottom: 1px solid #d9dde2 !important;
                            border-right: 0 !important;
                            border-radius: 0 !important;
                            background: #ffffff !important;
                            box-shadow: none !important;
                            display: flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            text-align: center !important;
                            color: inherit !important;
                            font-size: 14px !important;
                            font-weight: 400 !important;
                            line-height: 1.2 !important;
                            cursor: pointer !important;
                            white-space: nowrap !important;
                            overflow: hidden !important;
                            text-overflow: ellipsis !important;
                        }

                        .st-key-people_table [class*="st-key-edit_user_"] button:hover {
                            background: #f7f8fa !important;
                            border-top: 0 !important;
                            border-left-color: #d9dde2 !important;
                            border-bottom-color: #d9dde2 !important;
                            box-shadow: none !important;
                        }

                        .st-key-people_table [class*="st-key-edit_user_"] button p {
                            width: 100% !important;
                            margin: 0 !important;
                            padding: 0 !important;
                            text-align: center !important;
                            white-space: nowrap !important;
                            overflow: hidden !important;
                            text-overflow: ellipsis !important;
                        }

                        .st-key-people_table [data-testid="stHorizontalBlock"]:has(
                            [class*="st-key-edit_user_"]
                        ) [data-testid="stColumn"]:last-child button {
                            border-right: 1px solid #d9dde2 !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    # 헤더
                    header_col1, header_col2 = st.columns(
                        [employee_width, name_width],
                        gap=None
                    )

                    with header_col1:
                        st.markdown(
                            '<div class="people-grid-cell people-grid-header">사번</div>',
                            unsafe_allow_html=True
                        )

                    with header_col2:
                        st.markdown(
                            '<div class="people-grid-cell people-grid-header people-grid-cell-last">이름</div>',
                            unsafe_allow_html=True
                        )

                    # 데이터 행
                    for user in sorted_users:

                        row_col1, row_col2 = st.columns(
                            [employee_width, name_width],
                            gap=None
                        )

                        with row_col1:
                            if st.button(
                                str(user["employee_no"]),
                                key=f"edit_user_employee_{user['id']}",
                                use_container_width=True
                            ):
                                st.session_state["edit_user_id"] = user["id"]
                                safe_rerun()

                        with row_col2:
                            if st.button(
                                str(user["name"]),
                                key=f"edit_user_name_{user['id']}",
                                use_container_width=True
                            ):
                                st.session_state["edit_user_id"] = user["id"]
                                safe_rerun()

                    if not sorted_users:
                        st.info(
                            "등록된 인원이 없습니다."
                        )

                # --------------------------------------------------
                # 기존 수정 모달 연결
                # --------------------------------------------------

                edit_user_id = st.session_state.get(
                    "edit_user_id"
                )

                if edit_user_id:

                    edit_user = next(
                        (
                            user
                            for user in users_result
                            if user["id"] == edit_user_id
                        ),
                        None
                    )

                    if edit_user:
                        show_edit_user_dialog(
                            edit_user
                        )

        elif menu == "품목 관리":

            # 카테고리 불러오기
            categories_result = (
                admin_supabase
                .table("categories")
                .select("id, category_name, parent_id")
                .eq("is_active", True)
                .order("category_name")
                .execute()
            )

            categories = categories_result.data

            major_categories = [
                category
                for category in categories
                if category["parent_id"] is None
            ]

            major_category_options = {
                category["category_name"]: category["id"]
                for category in major_categories
            }

            # --------------------------------------------------
            # 상품 목록 조회 + 최신 분기 취합 설정 조회
            # --------------------------------------------------

            items_result = (
                admin_supabase
                .table("items")
                .select(
                    "id, store_name, product_code, item_name, category_id, "
                    "cost_price, is_active, created_at"
                )
                .eq("is_active", True)
                .order("item_name")
                .execute()
            )

            latest_quarter_result = (
                admin_supabase
                .table("quarters")
                .select("id, year, quarter")
                .order("year", desc=True)
                .order("quarter", desc=True)
                .limit(1)
                .execute()
            )

            latest_quarter_item_settings = {}

            if latest_quarter_result.data:

                latest_quarter_id = (
                    latest_quarter_result.data[0]["id"]
                )

                latest_settings_result = (
                    admin_supabase
                    .table("quarter_items")
                    .select(
                        "item_id, distribution_available, "
                        "disposal_available"
                    )
                    .eq(
                        "quarter_id",
                        latest_quarter_id
                    )
                    .execute()
                )

                latest_quarter_item_settings = {
                    row["item_id"]: row
                    for row in latest_settings_result.data
                }

            distribution_in_count = sum(
                1
                for item in items_result.data
                if latest_quarter_item_settings.get(
                    item["id"],
                    {}
                ).get(
                    "distribution_available",
                    False
                )
            )

            disposal_in_count = sum(
                1
                for item in items_result.data
                if latest_quarter_item_settings.get(
                    item["id"],
                    {}
                ).get(
                    "disposal_available",
                    False
                )
            )

            sorted_items = sorted(
                items_result.data,
                key=lambda x: x["item_name"]
            )

            # 실제 표시값을 먼저 만들어 각 열의 최대 길이를 계산
            item_rows = []

            for item in sorted_items:

                category_name = next(
                    (
                        category["category_name"]
                        for category in categories
                        if category["id"] == item["category_id"]
                    ),
                    "-"
                )

                setting = latest_quarter_item_settings.get(
                    item["id"],
                    {}
                )

                distribution_status = (
                    "IN"
                    if setting.get(
                        "distribution_available",
                        False
                    )
                    else "OUT"
                )

                disposal_status = (
                    "IN"
                    if setting.get(
                        "disposal_available",
                        False
                    )
                    else "OUT"
                )

                cost_text = (
                    f'{item["cost_price"]:,}원'
                    if item["cost_price"] is not None
                    else "-"
                )

                item_rows.append(
                    {
                        "item": item,
                        "values": [
                            str(item.get("store_name", "")),
                            str(item.get("product_code", "")),
                            str(item.get("item_name", "")),
                            cost_text,
                            category_name,
                            distribution_status,
                            disposal_status,
                        ]
                    }
                )

            item_headers = [
                "매장명",
                "상품코드",
                "상품명",
                "원가",
                "카테고리",
                "배분취합",
                "폐기취합",
            ]

            item_max_lengths = [
                max(
                    [len(item_headers[index])]
                    + [
                        len(row["values"][index])
                        for row in item_rows
                    ],
                    default=len(item_headers[index])
                )
                for index in range(len(item_headers))
            ]

            # 각 열의 최대 텍스트 길이를 기준으로 자연스러운 폭 계산
            item_widths = [
                max(92, item_max_lengths[0] * 9 + 28),
                max(105, item_max_lengths[1] * 9 + 28),
                max(150, item_max_lengths[2] * 9 + 28),
                max(95, item_max_lengths[3] * 9 + 28),
                max(105, item_max_lengths[4] * 10 + 28),
                max(105, item_max_lengths[5] * 10 + 28),
                max(105, item_max_lengths[6] * 10 + 28),
            ]

            items_table_width = sum(item_widths)

            # --------------------------------------------------
            # 상품 목록 제목 + 추가 버튼
            # 테이블과 동일한 부모 범위에서 우측 끝 정렬
            # --------------------------------------------------

            with st.container(key="items_header"):

                st.markdown(
                    """
                    <style>
                    /* 품목관리 헤더 영역에만 적용 */
                    .st-key-items_header {
                        width: 100% !important;
                        margin-bottom: 0 !important;
                    }

                    .st-key-items_header [data-testid="stHorizontalBlock"] {
                        gap: 0 !important;
                        margin: 0 !important;
                        padding: 0 !important;
                    }

                    .st-key-items_header [data-testid="stColumn"] {
                        padding-left: 0 !important;
                        padding-right: 0 !important;
                    }

                    .st-key-items_header [class*="st-key-open_add_items"] {
                        width: 100% !important;
                        display: flex !important;
                        justify-content: flex-end !important;
                        align-items: flex-start !important;
                    }

                    .st-key-items_header [class*="st-key-open_add_items"] button {
                        width: 32px !important;
                        height: 32px !important;
                        min-width: 32px !important;
                        min-height: 32px !important;
                        padding: 0 !important;
                        margin: 0 !important;
                        border-radius: 50% !important;
                        background: #2e8b57 !important;
                        border: none !important;
                        box-shadow: none !important;
                        color: #ffffff !important;
                        font-size: 20px !important;
                        font-weight: 900 !important;
                        line-height: 1 !important;
                        display: flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                    }

                    .st-key-items_header [class*="st-key-open_add_items"] button p {
                        color: #ffffff !important;
                        font-size: 20px !important;
                        font-weight: 900 !important;
                        line-height: 1 !important;
                        margin: 0 !important;
                        padding: 0 !important;
                        display: flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                        transform: translateY(-1px) !important;
                    }

                    .st-key-items_header [class*="st-key-open_add_items"] button:hover {
                        background: #26734a !important;
                        border: none !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                header_col1, header_col2 = st.columns(
                    [items_table_width - 44, 44],
                    gap=None
                )

                with header_col1:
                    st.subheader("상품 목록")
                    st.caption(
                        f"배분취합 IN {distribution_in_count}개  ·  "
                        f"폐기취합 IN {disposal_in_count}개"
                    )

                with header_col2:
                    if st.button(
                        "+",
                        key="open_add_items"
                    ):
                        st.session_state.bulk_item_dialog_version = (
                            st.session_state.get(
                                "bulk_item_dialog_version",
                                0
                            ) + 1
                        )

                        st.session_state.bulk_item_save_complete = False

                        show_add_items_dialog(
                            categories
                        )

            # --------------------------------------------------
            # 품목 목록 : 최대 데이터 길이에 맞춘 동적 열 너비
            # --------------------------------------------------

            if items_result.data:

                with st.container(key="items_table"):

                    st.markdown(
                        """
                        <style>
                        /* 품목관리 테이블 영역에만 적용 */
                        .st-key-items_table [data-testid="stVerticalBlock"],
                        .st-key-items_table [data-testid="stElementContainer"],
                        .st-key-items_table [data-testid="element-container"] {
                            gap: 0 !important;
                            margin: 0 !important;
                            padding-top: 0 !important;
                            padding-bottom: 0 !important;
                        }

                        .st-key-items_table [data-testid="stHorizontalBlock"] {
                            gap: 0 !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }

                        .st-key-items_table [data-testid="stColumn"] {
                            min-width: 0 !important;
                            width: auto !important;
                            margin: 0 !important;
                            padding-left: 0 !important;
                            padding-right: 0 !important;
                            box-sizing: border-box !important;
                        }

                        .st-key-items_table .items-grid-header {
                            width: 100%;
                            height: 44px !important;
                            min-height: 44px !important;
                            box-sizing: border-box;
                            display: flex;
                            align-items: center;
                            justify-content: center !important;
                            padding: 0 10px !important;
                            background: #f7f8fa;
                            border-top: 1px solid #d9dde2;
                            border-left: 1px solid #d9dde2;
                            border-bottom: 1px solid #d9dde2;
                            font-size: 14px;
                            font-weight: 700;
                            line-height: 1.2 !important;
                            text-align: center !important;
                            white-space: nowrap;
                            overflow: hidden;
                        }

                        .st-key-items_table .items-grid-header-last {
                            border-right: 1px solid #d9dde2;
                        }

                        .st-key-items_table [class*="st-key-edit_item_"] {
                            width: 100% !important;
                            height: 44px !important;
                            min-height: 44px !important;
                            margin: 0 !important;
                            padding: 0 !important;
                        }

                        .st-key-items_table [class*="st-key-edit_item_"] button {
                            width: 100% !important;
                            height: 44px !important;
                            min-height: 44px !important;
                            box-sizing: border-box !important;
                            padding: 0 10px !important;
                            margin: 0 !important;
                            border-top: 0 !important;
                            border-left: 1px solid #d9dde2 !important;
                            border-bottom: 1px solid #d9dde2 !important;
                            border-right: 0 !important;
                            border-radius: 0 !important;
                            background: #ffffff !important;
                            box-shadow: none !important;
                            color: inherit !important;
                            display: flex !important;
                            align-items: center !important;
                            justify-content: center !important;
                            font-size: 14px !important;
                            font-weight: 400 !important;
                            line-height: 1.2 !important;
                            text-align: center !important;
                            white-space: nowrap !important;
                            overflow: hidden !important;
                            text-overflow: ellipsis !important;
                            cursor: pointer !important;
                        }

                        .st-key-items_table [class*="st-key-edit_item_"] button:hover {
                            background: #f7f8fa !important;
                            border-top: 0 !important;
                            border-left-color: #d9dde2 !important;
                            border-bottom-color: #d9dde2 !important;
                            box-shadow: none !important;
                        }

                        .st-key-items_table [class*="st-key-edit_item_"] button p {
                            width: 100% !important;
                            margin: 0 !important;
                            padding: 0 !important;
                            text-align: center !important;
                            overflow: hidden !important;
                            text-overflow: ellipsis !important;
                            white-space: nowrap !important;
                        }

                        .st-key-items_table [data-testid="stHorizontalBlock"]:has(
                            [class*="st-key-edit_item_"]
                        ) [data-testid="stColumn"]:last-child button {
                            border-right: 1px solid #d9dde2 !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    # 헤더
                    header_columns = st.columns(
                        item_widths,
                        gap=None
                    )

                    for index, (header_col, header_text) in enumerate(
                        zip(header_columns, item_headers)
                    ):
                        with header_col:
                            last_class = (
                                " items-grid-header-last"
                                if index == len(item_headers) - 1
                                else ""
                            )

                            st.markdown(
                                f'<div class="items-grid-header{last_class}">{header_text}</div>',
                                unsafe_allow_html=True
                            )

                    # 데이터 행
                    for row in item_rows:

                        item = row["item"]
                        row_values = row["values"]

                        row_columns = st.columns(
                            item_widths,
                            gap=None
                        )

                        for col_index, (row_col, cell_value) in enumerate(
                            zip(row_columns, row_values),
                            start=1
                        ):
                            with row_col:

                                if st.button(
                                    cell_value,
                                    key=(
                                        f"edit_item_{item['id']}_"
                                        f"cell_{col_index}"
                                    ),
                                    use_container_width=True
                                ):
                                    st.session_state.edit_item_id = item["id"]
                                    safe_rerun()

                # --------------------------------------------------
                # 상품 수정 모달
                # --------------------------------------------------

                edit_item_id = st.session_state.get(
                    "edit_item_id"
                )

                if edit_item_id:

                    edit_item = next(
                        (
                            item
                            for item in items_result.data
                            if item["id"] == edit_item_id
                        ),
                        None
                    )

                    if edit_item:

                        show_edit_item_dialog(
                            edit_item,
                            categories,
                            major_categories
                        )

            else:
                st.info("등록된 상품이 없습니다.")

        elif menu == "분기/취합 관리":

            # ==================================================
            # 분기/취합 관리 메인 영역
            # 좌측 40% : 분기 목록
            # 우측 60% : 분기별 품목 취합 설정
            # ==================================================

            st.markdown(
                """
                <style>
                .st-key-quarter_manage_page {
                    width: 100% !important;
                    box-sizing: border-box !important;
                }

                /* 분기/취합 관리 페이지 내부 전용 스타일 */
                .st-key-quarter_manage_page .quarter-main-grid {
                    display: grid;
                    grid-template-columns: 40% 60%;
                    width: 100%;
                    box-sizing: border-box;
                    gap: 24px;
                    align-items: start;
                }

                /* 분기 목록의 헤더 및 데이터 텍스트 */
                .st-key-quarter_manage_page .quarter-list-header {
                    width: 100% !important;
                    box-sizing: border-box !important;
                    text-align: center !important;
                    font-weight: 700 !important;
                }

                /* 분기 생성 / 품목 설정 저장 버튼만 pill 스타일 적용 */
                .st-key-quarter_manage_page [class*="st-key-open_create_quarter"] button,
                .st-key-quarter_manage_page [class*="st-key-save_quarter_item_settings"] button {
                    background: #2e8b57 !important;
                    color: #ffffff !important;
                    font-weight: 500 !important;
                    font-size: 14px !important;
                    padding: 0 16px !important;
                    min-height: 32px !important;
                    height: 32px !important;
                    border: none !important;
                    border-radius: 9999px !important;
                    box-sizing: border-box !important;
                    box-shadow: none !important;
                }

                .st-key-quarter_manage_page [class*="st-key-open_create_quarter"] button:hover,
                .st-key-quarter_manage_page [class*="st-key-save_quarter_item_settings"] button:hover {
                    background: #26734a !important;
                    color: #ffffff !important;
                    border: none !important;
                    box-shadow: none !important;
                }

                .st-key-quarter_manage_page [class*="st-key-open_create_quarter"] button p {
                    color: #ffffff !important;
                    font-weight: 900 !important;
                    font-size: 18px !important;
                    margin: 0 !important;
                    line-height: 1 !important;
                }

                /* 저장 버튼은 테이블 우측 끝선에 맞춰 오른쪽 정렬 */
                .st-key-quarter_manage_page .st-key-quarter_setting_save_row {
                    width: 100% !important;
                }

                .st-key-quarter_manage_page .st-key-quarter_setting_save_row [class*="st-key-save_quarter_item_settings"] {
                    display: flex !important;
                    justify-content: flex-end !important;
                    width: 100% !important;
                }

                .st-key-quarter_manage_page [class*="st-key-save_quarter_item_settings"] button {
                    width: fit-content !important;
                    min-width: fit-content !important;
                    max-width: fit-content !important;
                }

                .st-key-quarter_manage_page [class*="st-key-save_quarter_item_settings"] button p {
                    color: #ffffff !important;
                    font-weight: 500 !important;
                    font-size: 14px !important;
                    margin: 0 !important;
                    white-space: nowrap !important;
                }

                .st-key-quarter_manage_page [class*="st-key-open_create_quarter"] button {
                    width: 32px !important;
                    min-width: 32px !important;
                    max-width: 32px !important;
                    padding: 0 !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                }

                /* 분기 목록의 분기/취합기간 텍스트 자체를 클릭 영역으로 사용 */
                .st-key-quarter_manage_page [class*="st-key-open_manage_quarter_"] button {
                    width: 100% !important;
                    min-height: 40px !important;
                    padding: 0 !important;
                    margin: 0 !important;
                    background: transparent !important;
                    border: none !important;
                    box-shadow: none !important;
                    color: inherit !important;
                    font-size: 17px !important;
                    font-weight: 400 !important;
                    text-align: center !important;
                    cursor: pointer !important;
                }

                .st-key-quarter_manage_page [class*="st-key-open_manage_quarter_"] button p {
                    width: 100% !important;
                    margin: 0 !important;
                    text-align: center !important;
                    font-size: 17px !important;
                    font-weight: 400 !important;
                }

                .st-key-quarter_manage_page [class*="st-key-open_manage_quarter_"] button:hover {
                    background: #f7f8fa !important;
                    border: none !important;
                    box-shadow: none !important;
                }

                /* 분기별 품목 취합 설정 영역 내부 전용 정렬 */
                .st-key-quarter_setting_select label,
                .st-key-quarter_setting_select label p,
                .st-key-quarter_setting_select label span {
                    font-weight: 700 !important;
                }

                /* Streamlit BaseWeb Select의 실제 표시 텍스트까지 강제 볼드 */
                .st-key-quarter_setting_select [data-testid="stSelectbox"] {
                    width: fit-content !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                }

                .st-key-quarter_setting_select [data-baseweb="select"] {
                    width: fit-content !important;
                    min-width: 0 !important;
                    max-width: 100% !important;
                    font-weight: 700 !important;
                }

                /* Streamlit/BaseWeb Select 실제 표시 텍스트 강제 볼드 */
                .st-key-quarter_setting_select [data-baseweb="select"],
                .st-key-quarter_setting_select [data-baseweb="select"] *,
                .st-key-quarter_setting_select [data-baseweb="select"] [role="combobox"],
                .st-key-quarter_setting_select [data-baseweb="select"] [role="combobox"] *,
                .st-key-quarter_setting_select [data-baseweb="select"] input,
                .st-key-quarter_setting_select [data-baseweb="select"] span,
                .st-key-quarter_setting_select [data-baseweb="select"] div {
                    font-weight: 700 !important;
                }

                /* BaseWeb에서 선택값을 렌더링하는 모든 일반 텍스트 노드의 부모 */
                .st-key-quarter_setting_select [data-baseweb="select"] [class*="singleValue"],
                .st-key-quarter_setting_select [data-baseweb="select"] [class*="placeholder"],
                .st-key-quarter_setting_select [data-baseweb="select"] [class*="valueContainer"],
                .st-key-quarter_setting_select [data-baseweb="select"] [data-baseweb="value-container"] {
                    font-weight: 700 !important;
                }

                /* 분기별 품목 취합 설정 셀 그리드 */
                .st-key-quarter_setting_table [data-testid="stVerticalBlock"],
                .st-key-quarter_setting_table [data-testid="stElementContainer"],
                .st-key-quarter_setting_table [data-testid="element-container"] {
                    gap: 0 !important;
                    margin: 0 !important;
                    padding-top: 0 !important;
                    padding-bottom: 0 !important;
                }

                .st-key-quarter_setting_table [data-testid="stHorizontalBlock"] {
                    gap: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                .st-key-quarter_setting_table [data-testid="stColumn"] {
                    min-width: 0 !important;
                    margin: 0 !important;
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                    box-sizing: border-box !important;
                }

                .st-key-quarter_setting_table .quarter-setting-grid-cell {
                    width: 100% !important;
                    height: 44px !important;
                    min-height: 44px !important;
                    max-height: 44px !important;
                    box-sizing: border-box !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                    padding: 0 10px !important;
                    margin: 0 !important;
                    background: #ffffff !important;
                    border-top: 1px solid #d9dde2 !important;
                    border-left: 1px solid #d9dde2 !important;
                    border-bottom: 1px solid #d9dde2 !important;
                    font-size: 14px !important;
                    line-height: 1.2 !important;
                    text-align: center !important;
                    white-space: nowrap !important;
                    overflow: hidden !important;
                }

                .st-key-quarter_setting_table .quarter-setting-grid-header {
                    background: #f7f8fa !important;
                    font-weight: 700 !important;
                }

                .st-key-quarter_setting_table .quarter-setting-grid-cell-last {
                    border-right: 1px solid #d9dde2 !important;
                }

                /* 체크박스 셀도 동일한 높이/테두리를 유지 */
                .st-key-quarter_setting_table [class*="st-key-quarter_distribution_cell_"],
                .st-key-quarter_setting_table [class*="st-key-quarter_disposal_cell_"] {
                    width: 100% !important;
                    height: 44px !important;
                    min-height: 44px !important;
                    max-height: 44px !important;
                    box-sizing: border-box !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    background: #ffffff !important;
                    border-top: 1px solid #d9dde2 !important;
                    border-left: 1px solid #d9dde2 !important;
                    border-bottom: 1px solid #d9dde2 !important;
                    display: flex !important;
                    align-items: center !important;
                    justify-content: center !important;
                }

                .st-key-quarter_setting_table [class*="st-key-quarter_disposal_cell_"] {
                    border-right: 1px solid #d9dde2 !important;
                }

                .st-key-quarter_setting_table [class*="st-key-quarter_distribution_cell_"] [data-testid="stCheckbox"],
                .st-key-quarter_setting_table [class*="st-key-quarter_disposal_cell_"] [data-testid="stCheckbox"] {
                    width: 100% !important;
                    height: 100% !important;
                    display: flex !important;
                    justify-content: center !important;
                    align-items: center !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                .st-key-quarter_setting_table [class*="st-key-quarter_distribution_cell_"] [data-testid="stCheckbox"] label,
                .st-key-quarter_setting_table [class*="st-key-quarter_disposal_cell_"] [data-testid="stCheckbox"] label {
                    width: auto !important;
                    display: flex !important;
                    justify-content: center !important;
                    align-items: center !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                /* 저장 버튼: 헤더와 테이블의 동일한 우측 기준선 사용 */
                .st-key-quarter_setting_header {
                    width: 100% !important;
                    max-width: 100% !important;
                    box-sizing: border-box !important;
                    margin: 0 !important;
                    padding: 0 !important;
                }

                .st-key-quarter_setting_header [data-testid="stHorizontalBlock"] {
                    width: 100% !important;
                    max-width: 100% !important;
                    gap: 0 !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    align-items: center !important;
                    box-sizing: border-box !important;
                }

                .st-key-quarter_setting_header [data-testid="stColumn"] {
                    margin: 0 !important;
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                    box-sizing: border-box !important;
                }

                /* 실제 저장 버튼이 들어있는 마지막 컬럼을 직접 찾아 오른쪽 끝 정렬 */
                .st-key-quarter_setting_header [data-testid="stColumn"]:has([data-testid="stButton"]) {
                    display: flex !important;
                    justify-content: flex-end !important;
                    align-items: center !important;
                    margin-left: 0 !important;
                    margin-right: 0 !important;
                    padding-left: 0 !important;
                    padding-right: 0 !important;
                    box-sizing: border-box !important;
                }

                .st-key-quarter_setting_header [data-testid="stColumn"]:has([data-testid="stButton"]) > div {
                    width: 100% !important;
                    max-width: 100% !important;
                    display: flex !important;
                    justify-content: flex-end !important;
                    align-items: center !important;
                    margin: 0 !important;
                    padding: 0 !important;
                    box-sizing: border-box !important;
                }

                .st-key-quarter_setting_header [data-testid="stButton"] {
                    width: fit-content !important;
                    max-width: fit-content !important;
                    min-width: 0 !important;
                    margin: 0 0 0 auto !important;
                    padding: 0 !important;
                    display: flex !important;
                    justify-content: flex-end !important;
                    box-sizing: border-box !important;
                }

                .st-key-quarter_setting_header [data-testid="stButton"] button {
                    width: fit-content !important;
                    min-width: fit-content !important;
                    max-width: fit-content !important;
                    margin: 0 !important;
                }

                .st-key-quarter_setting_header [data-testid="stButton"] button p {
                    white-space: nowrap !important;
                    margin: 0 !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            with st.container(key="quarter_manage_page"):

                # ==================================================
                # 분기 목록 조회
                # ==================================================

                quarters_result = (
                    admin_supabase
                    .table("quarters")
                    .select(
                        "id, year, quarter, start_date, end_date, status"
                    )
                    .order("year", desc=True)
                    .order("quarter", desc=True)
                    .execute()
                )

                # Streamlit 위젯을 동일한 40:60 구조로 배치
                left_area, right_area = st.columns(
                    [4, 6],
                    gap="medium"
                )

                with left_area:

                    header_col1, header_col2 = st.columns([5, 1])

                    with header_col1:
                        st.subheader("분기 목록")

                    with header_col2:

                        if st.button(
                            "+",
                            type="primary",
                            use_container_width=True,
                            key="open_create_quarter"
                        ):
                            show_create_quarter_dialog()

                    if quarters_result.data:

                        list_col1, list_col2 = st.columns(
                            [2, 3]
                        )

                        with list_col1:
                            st.markdown(
                                '<div class="quarter-list-header">분기</div>',
                                unsafe_allow_html=True
                            )

                        with list_col2:
                            st.markdown(
                                '<div class="quarter-list-header">취합 기간</div>',
                                unsafe_allow_html=True
                            )

                        st.divider()

                        for q in quarters_result.data:

                            row_col1, row_col2 = st.columns(
                                [2, 3]
                            )

                            with row_col1:
                                if st.button(
                                    f"{q['year']}년 {q['quarter']}분기",
                                    key=f"open_manage_quarter_name_{q['id']}",
                                    use_container_width=True
                                ):
                                    show_quarter_manage_dialog(q)

                            with row_col2:
                                if st.button(
                                    f"{q['start_date']} ~ {q['end_date']}",
                                    key=f"open_manage_quarter_date_{q['id']}",
                                    use_container_width=True
                                ):
                                    show_quarter_manage_dialog(q)

                    else:
                        st.info("등록된 분기가 없습니다.")

                with right_area:

                    # ==================================================
                    # 분기별 품목 취합 설정
                    # ==================================================

                    if quarters_result.data:

                        with st.container(key="quarter_setting_header"):
                            setting_header_col1, setting_header_col2 = st.columns(
                                [8, 2],
                                gap=None
                            )

                            with setting_header_col1:
                                st.subheader("분기별 품목 취합 설정")

                            with setting_header_col2:
                                save_settings_clicked = st.button(
                                    "저장",
                                    type="primary",
                                    key="save_quarter_item_settings"
                                )

                        (
                            selected_item_setting_major,
                            selected_item_setting_detail,
                            selected_item_setting_quarter_id,
                            _
                        ) = render_hierarchical_quarter_selector(
                            quarters_result.data,
                            label="설정할 분기",
                            major_key="quarter_item_setting_major",
                            detail_key="quarter_item_setting_detail",
                            include_new_hire=False,
                            include_all=False
                        )

                        items_result = (
                            admin_supabase
                            .table("items")
                            .select("id, item_name, product_code")
                            .eq("is_active", True)
                            .order("item_name")
                            .execute()
                        )

                        # 상품명 기준 오름차순을 화면 표시 순서로 고정
                        quarter_setting_items = sorted(
                            items_result.data or [],
                            key=lambda item: str(
                                item.get("item_name", "")
                            )
                        )

                        existing_result = (
                            admin_supabase
                            .table("quarter_items")
                            .select(
                                "item_id, distribution_available, disposal_available"
                            )
                            .eq(
                                "quarter_id",
                                selected_item_setting_quarter_id
                            )
                            .execute()
                        )

                        existing_items = {
                            row["item_id"]: row
                            for row in existing_result.data
                        }

                        st.write(
                            "품목별 취합 노출 여부를 설정하세요."
                        )

                        with st.container(key="quarter_setting_table"):

                            header_col1, header_col2, header_col3, header_col4 = st.columns(
                                [2, 4, 2, 2],
                                gap=None
                            )

                            with header_col1:
                                st.markdown(
                                    '<div class="quarter-setting-grid-cell quarter-setting-grid-header">상품코드</div>',
                                    unsafe_allow_html=True
                                )

                            with header_col2:
                                st.markdown(
                                    '<div class="quarter-setting-grid-cell quarter-setting-grid-header">상품명</div>',
                                    unsafe_allow_html=True
                                )

                            with header_col3:
                                st.markdown(
                                    '<div class="quarter-setting-grid-cell quarter-setting-grid-header">배분 취합</div>',
                                    unsafe_allow_html=True
                                )

                            with header_col4:
                                st.markdown(
                                    '<div class="quarter-setting-grid-cell quarter-setting-grid-header quarter-setting-grid-cell-last">폐기 취합</div>',
                                    unsafe_allow_html=True
                                )

                            settings = []

                            for item in quarter_setting_items:

                                existing = existing_items.get(
                                    item["id"],
                                    {}
                                )

                                distribution_default = existing.get(
                                    "distribution_available",
                                    True
                                )

                                disposal_default = existing.get(
                                    "disposal_available",
                                    True
                                )

                                col1, col2, col3, col4 = st.columns(
                                    [2, 4, 2, 2]
                                )

                                with col1:
                                    st.markdown(
                                        f'<div class="quarter-setting-grid-cell">{item["product_code"]}</div>',
                                        unsafe_allow_html=True
                                    )

                                with col2:
                                    st.markdown(
                                        f'<div class="quarter-setting-grid-cell">{item["item_name"]}</div>',
                                        unsafe_allow_html=True
                                    )

                                with col3:
                                    with st.container(
                                        key=f"quarter_distribution_cell_{selected_item_setting_quarter_id}_{item['id']}"
                                    ):
                                        distribution = st.checkbox(
                                            "",
                                            value=distribution_default,
                                            key=(
                                                f"distribution_"
                                                f"{selected_item_setting_quarter_id}_"
                                                f"{item['id']}"
                                            )
                                        )

                                with col4:
                                    with st.container(
                                        key=f"quarter_disposal_cell_{selected_item_setting_quarter_id}_{item['id']}"
                                    ):
                                        disposal = st.checkbox(
                                            "",
                                            value=disposal_default,
                                            key=(
                                                f"disposal_"
                                                f"{selected_item_setting_quarter_id}_"
                                                f"{item['id']}"
                                            )
                                        )

                                settings.append({
                                    "quarter_id": selected_item_setting_quarter_id,
                                    "item_id": item["id"],
                                    "distribution_available": distribution,
                                    "disposal_available": disposal
                                })

                        if save_settings_clicked:

                            try:
                                with loading_guard(
                                    "분기별 품목 취합 설정 저장 중..."
                                ):
                                    for setting in settings:
                                        admin_supabase.table(
                                            "quarter_items"
                                        ).upsert(
                                            setting,
                                            on_conflict="quarter_id,item_id"
                                        ).execute()

                            except Exception as e:
                                st.error("품목 설정 저장 실패")
                                st.write(e)
                            else:
                                show_item_setting_save_complete()

                    else:
                        st.info("등록된 분기가 없습니다.")


        elif menu == "발주/배분 관리":

            quarter_result = (
                admin_supabase
                .table("quarters")
                .select("id, year, quarter, status")
                .order(
                    "year",
                    desc=True
                )
                .order(
                    "quarter",
                    desc=True
                )
                .execute()
            )

            if not quarter_result.data:

                st.warning(
                    "등록된 분기가 없습니다."
                )

            else:

                (
                    selected_order_major,
                    selected_order_detail,
                    selected_quarter_id,
                    _
                ) = render_hierarchical_quarter_selector(
                    quarter_result.data,
                    label="발주할 분기",
                    major_key="order_quarter_major",
                    detail_key="order_quarter_detail",
                    include_new_hire=False,
                    include_all=False
                )

                if selected_quarter_id is None:
                    st.warning("분기를 선택해주세요.")
                    st.stop()

                st.markdown(
                    """
                    <style>
                    /* 발주/배분 관리 - 발주할 분기 선택 영역에만 적용 */
                    .st-key-hierarchical_selector_order_quarter_major {
                        width: max-content !important;
                        max-width: max-content !important;
                    }

                    .st-key-hierarchical_selector_order_quarter_major label {
                        font-weight: 700 !important;
                        font-size: 22px !important;
                    }

                    .st-key-hierarchical_selector_order_quarter_major [data-testid="stWidgetLabel"] p,
                    .st-key-hierarchical_selector_order_quarter_major [data-testid="stWidgetLabel"] span {
                        font-weight: 700 !important;
                        font-size: 22px !important;
                    }

                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"],
                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"] > div {
                        width: max-content !important;
                        min-width: 0 !important;
                    }

                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"] > div {
                        display: inline-flex !important;
                    }

                    /* 분기 선택 바 내부 텍스트를 취합 결과 제목과 동일한 22px로 적용 */
                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"] *,
                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"] [role="combobox"],
                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"] [class*="singleValue"],
                    .st-key-hierarchical_selector_order_quarter_major [data-baseweb="select"] [class*="valueContainer"] {
                        font-size: 22px !important;
                        font-weight: 700 !important;
                    }

                    /* 취합 결과 상품명: 셀 너비 안에서만 줄바꿈 */
                    .order-result-product-name {
                        white-space: normal !important;
                        word-break: break-all !important;
                        overflow-wrap: anywhere !important;
                        line-height: 1.45 !important;
                    }

                    /* 발주여부 체크박스 셀: 모든 행 동일하게 중앙 정렬 */
                    [class*='st-key-order_status_cell_'] {
                        width: 100% !important;
                    }

                    [class*='st-key-order_status_cell_'] {
                        width: 100% !important;
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                        text-align: center !important;
                    }

                    [class*='st-key-order_status_cell_'] > div,
                    [class*='st-key-order_status_cell_'] [data-testid="stCheckbox"] {
                        width: 100% !important;
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                        margin: 0 !important;
                    }

                    [class*='st-key-order_status_cell_'] [data-testid="stCheckbox"] > label {
                        width: 100% !important;
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                        margin: 0 !important;
                        padding: 0 !important;
                    }

                    [class*='st-key-order_status_cell_'] [data-testid="stCheckbox"] > label > div:first-child {
                        margin-left: auto !important;
                        margin-right: auto !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                left_col, right_col = st.columns(
                    [3, 2],
                    gap="large"
                )

                with left_col:

                    with st.container(key="order_collection_result"):

                        st.markdown(
                            """
                            <style>
                            /* 발주/배분 관리 - 취합 결과 영역에만 적용 */
                            .st-key-order_collection_result [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] {
                                display: flex !important;
                                flex-direction: column !important;
                                justify-content: center !important;
                                align-items: center !important;
                                text-align: center !important;
                            }

                            .st-key-order_collection_result [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] > div {
                                width: 100% !important;
                                text-align: center !important;
                            }

                            .st-key-order_collection_result [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] p,
                            .st-key-order_collection_result [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] div,
                            .st-key-order_collection_result [data-testid="stHorizontalBlock"] > [data-testid="stColumn"] span {
                                text-align: center !important;
                            }

                            /* 상품코드 데이터의 시작점을 취합 결과 제목의 시작선과 정확히 맞춤 */
                            .st-key-order_collection_result .order-result-product-code {
                                width: 100% !important;
                                margin: 0 !important;
                                padding: 0 !important;
                                text-align: left !important;
                                display: block !important;
                            }

                            /* 총 취합수량은 해당 열의 헤더 정중앙과 동일한 기준선에 배치 */
                            .st-key-order_collection_result [class*="st-key-order_result_quantity_cell_"] {
                                width: 100% !important;
                                margin: 0 !important;
                                padding: 0 !important;
                                display: flex !important;
                                justify-content: center !important;
                                align-items: center !important;
                                text-align: center !important;
                            }

                            .st-key-order_collection_result [class*="st-key-order_result_quantity_cell_"] > div,
                            .st-key-order_collection_result [class*="st-key-order_result_quantity_cell_"] [data-testid="stPopover"] {
                                width: auto !important;
                                margin-left: auto !important;
                                margin-right: auto !important;
                            }

                            /* 발주할 분기 라벨 볼드 강제 */
                            .st-key-hierarchical_selector_order_quarter_major label,
                            .st-key-hierarchical_selector_order_quarter_major [data-testid="stWidgetLabel"] p {
                                font-weight: 700 !important;
                            }

                            /* 총 취합수량 인원 상세 보기 버튼 */
                            .st-key-order_collection_result [data-testid="stPopover"] button {
                                width: fit-content !important;
                                min-width: 0 !important;
                                max-width: none !important;
                                padding: 0 !important;
                                margin: 0 auto !important;
                                border: 0 !important;
                                background: transparent !important;
                                box-shadow: none !important;
                                color: #4f46e5 !important;
                                font-size: 14px !important;
                                font-weight: 700 !important;
                                line-height: 1.2 !important;
                                white-space: nowrap !important;
                                display: inline-flex !important;
                                justify-content: center !important;
                                align-items: center !important;
                                cursor: pointer !important;
                            }

                            .st-key-order_collection_result [data-testid="stPopover"] button:hover {
                                color: #3730a3 !important;
                                text-decoration: underline !important;
                                background: transparent !important;
                            }

                            .st-key-order_collection_result [data-testid="stPopover"] button p {
                                font-size: 14px !important;
                                font-weight: 700 !important;
                                margin: 0 !important;
                                padding: 0 !important;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )

                        # ==================================================
                        # 취합 결과
                        # ==================================================

                        st.subheader(
                            "취합 결과"
                        )

                        header_col1, header_col2, header_col3, header_col4 = st.columns(
                            [2, 4, 2, 1]
                        )

                        with header_col1:

                            st.markdown(
                                "**상품코드**"
                            )

                        with header_col2:

                            st.markdown(
                                "**상품명**"
                            )

                        with header_col3:

                            st.markdown(
                                "**총 취합수량**"
                            )

                        with header_col4:

                            st.markdown(
                                "**발주여부**"
                            )

                        requests_result = (
                            admin_supabase
                            .table("requests")
                            .select(
                                "user_id, item_id, requested_qty, "
                                "items(item_name, product_code, cost_price)"
                            )
                            .eq(
                                "quarter_id",
                                selected_quarter_id
                            )
                            .execute()
                        )

                        if requests_result.data:

                            collection_result = {}

                            for row in requests_result.data:

                                item_id = row["item_id"]

                                if item_id not in collection_result:

                                    collection_result[item_id] = {
                                        "item_id": item_id,
                                        "item_name": row["items"]["item_name"],
                                        "product_code": row["items"]["product_code"],
                                        "cost_price": row["items"]["cost_price"],
                                        "requested_qty": 0
                                    }

                                collection_result[item_id][
                                    "requested_qty"
                                ] += row["requested_qty"]

                            sorted_items = sorted(
                                collection_result.values(),
                                key=lambda x: x["requested_qty"],
                                reverse=True
                            )

                            def render_collection_detail(
                                selected_quarter_id,
                                item_id,
                                requested_qty
                            ):

                                with st.popover(
                                    f"{requested_qty}개",
                                    use_container_width=False
                                ):

                                    user_requests_result = (
                                        admin_supabase
                                        .table("requests")
                                        .select(
                                            "user_id, requested_qty, "
                                            "users(name, employee_no)"
                                        )
                                        .eq(
                                            "quarter_id",
                                            selected_quarter_id
                                        )
                                        .eq(
                                            "item_id",
                                            item_id
                                        )
                                        .execute()
                                    )

                                    st.caption(
                                        f"취합 인원 ({len(user_requests_result.data)}명)"
                                    )

                                    if user_requests_result.data:

                                        for row in sorted(
                                            user_requests_result.data,
                                            key=lambda x: (
                                                x["users"]["name"]
                                                if x.get("users")
                                                else ""
                                            )
                                        ):

                                            user_info = row.get("users")

                                            if not user_info:
                                                continue

                                            st.write(
                                                f"• {user_info['name']} "
                                                f"({user_info['employee_no']})"
                                            )

                                    else:

                                        st.write(
                                            "취합한 인원이 없습니다."
                                        )

                            # 현재 분기의 최신 draft 발주 1개 조회
                            draft_check_result = (
                                admin_supabase
                                .table("orders")
                                .select("id")
                                .eq(
                                    "quarter_id",
                                    selected_quarter_id
                                )
                                .eq(
                                    "status",
                                    "draft"
                                )
                                .order(
                                    "created_at",
                                    desc=True
                                )
                                .limit(1)
                                .execute()
                            )

                            draft_order_id = (
                                draft_check_result.data[0]["id"]
                                if draft_check_result.data
                                else None
                            )

                            # 발주 목록에 이미 들어간 item_id 조회
                            draft_order_item_ids = set()

                            if draft_order_id:

                                draft_order_items_result = (
                                    admin_supabase
                                    .table("order_items")
                                    .select("item_id")
                                    .eq(
                                        "order_id",
                                        draft_order_id
                                    )
                                    .execute()
                                )

                                draft_order_item_ids = {
                                    row["item_id"]
                                    for row in draft_order_items_result.data
                                }

                            for item in sorted_items:

                                col1, col2, col3, col4 = st.columns(
                                    [2, 4, 2, 1]
                                )

                                with col1:

                                    st.markdown(
                                        f'<div class="order-result-product-code">{html.escape(str(item["product_code"]))}</div>',
                                        unsafe_allow_html=True
                                    )

                                with col2:

                                    st.markdown(
                                        f'<div class="order-result-product-name">{html.escape(str(item["item_name"]))}</div>',
                                        unsafe_allow_html=True
                                    )

                                with col3:

                                    with st.container(
                                        key=f"order_result_quantity_cell_{selected_quarter_id}_{item['item_id']}"
                                    ):
                                        render_collection_detail(
                                            selected_quarter_id,
                                            item["item_id"],
                                            item["requested_qty"]
                                        )

                                with col4:

                                    order_status_key = (
                                        f"order_status_{selected_quarter_id}_{item['item_id']}"
                                    )

                                    def toggle_order_status(
                                        quarter_id,
                                        item_id,
                                        state_key,
                                        cost_price
                                    ):

                                        checked = st.session_state.get(
                                            state_key,
                                            False
                                        )

                                        current_draft_result = (
                                            admin_supabase
                                            .table("orders")
                                            .select("id")
                                            .eq(
                                                "quarter_id",
                                                quarter_id
                                            )
                                            .eq(
                                                "status",
                                                "draft"
                                            )
                                            .order(
                                                "created_at",
                                                desc=True
                                            )
                                            .limit(1)
                                            .execute()
                                        )

                                        current_draft_id = (
                                            current_draft_result.data[0]["id"]
                                            if current_draft_result.data
                                            else None
                                        )

                                        if checked:

                                            if not current_draft_id:

                                                active_users_result = (
                                                    admin_supabase
                                                    .table("users")
                                                    .select("id")
                                                    .eq(
                                                        "is_active",
                                                        True
                                                    )
                                                    .execute()
                                                )

                                                active_user_count = len(
                                                    active_users_result.data
                                                )

                                                new_order_result = (
                                                    admin_supabase
                                                    .table("orders")
                                                    .insert(
                                                        {
                                                            "quarter_id": quarter_id,
                                                            "distribution_user_count": active_user_count,
                                                            "status": "draft"
                                                        }
                                                    )
                                                    .execute()
                                                )

                                                current_draft_id = (
                                                    new_order_result.data[0]["id"]
                                                )

                                            existing_item_result = (
                                                admin_supabase
                                                .table("order_items")
                                                .select("id")
                                                .eq(
                                                    "order_id",
                                                    current_draft_id
                                                )
                                                .eq(
                                                    "item_id",
                                                    item_id
                                                )
                                                .limit(1)
                                                .execute()
                                            )

                                            if not existing_item_result.data:

                                                (
                                                    admin_supabase
                                                    .table("order_items")
                                                    .insert(
                                                        {
                                                            "order_id": current_draft_id,
                                                            "item_id": item_id,
                                                            "cost_price": cost_price,
                                                            "order_quantity": 0,
                                                            "per_user_quantity": 0
                                                        }
                                                    )
                                                    .execute()
                                                )

                                        else:

                                            if current_draft_id:

                                                (
                                                    admin_supabase
                                                    .table("order_items")
                                                    .delete()
                                                    .eq(
                                                        "order_id",
                                                        current_draft_id
                                                    )
                                                    .eq(
                                                        "item_id",
                                                        item_id
                                                    )
                                                    .execute()
                                                )

                                    with st.container(
                                        key=f"order_status_cell_{selected_quarter_id}_{item['item_id']}"
                                    ):

                                        st.checkbox(
                                            "",
                                            value=(
                                                item["item_id"]
                                                in draft_order_item_ids
                                            ),
                                            key=order_status_key,
                                            label_visibility="collapsed",
                                            on_change=toggle_order_status,
                                            args=(
                                                selected_quarter_id,
                                                item["item_id"],
                                                order_status_key,
                                                item.get("cost_price", 0)
                                            )
                                        )
                        else:

                            st.write(
                                "아직 취합된 요청이 없습니다."
                            )

                    st.divider()


                with right_col:

                    header_col1, header_col2 = st.columns(
                        [5, 1]
                    )

                    with header_col1:

                        st.subheader(
                            "발주/배분 관리"
                        )

                    with header_col2:

                        with st.container(key="order_action_button"):

                            if st.button(
                                    "발주",
                                    type="primary",
                                    use_container_width=True,
                                    key="open_order_items"
                                ):

                                st.session_state["order_dialog_instance"] = (
                                    st.session_state.get(
                                        "order_dialog_instance",
                                        0
                                    ) + 1
                                )

                                st.session_state.pop(
                                    "order_dialog_result_message",
                                    None
                                )
                                st.session_state.pop(
                                    "order_dialog_result_type",
                                    None
                                )
                                st.session_state.pop(
                                    "receive_all",
                                    None
                                )
                                # 발주 화면 진입 시 신규입사 모드는 항상 해제 상태로 시작합니다.
                                # 현재 실행에서는 아직 위젯이 생성되기 전이므로 False 지정이 안전합니다.
                                st.session_state[
                                    "new_hire_distribution_mode"
                                ] = False
                                st.session_state.pop(
                                    "new_hire_batch_label",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_selected_item_labels",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_distribution_result",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_pending_batch_id",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_distribution_title",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_pasted_text",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_pasted_source",
                                    None
                                )
                                st.session_state.pop(
                                    "new_hire_pasted_rows",
                                    None
                                )

                                for state_key in list(
                                    st.session_state.keys()
                                ):
                                    if (
                                        state_key.startswith("receive_")
                                        or state_key.startswith("per_user_qty_")
                                        or state_key.startswith("order_memo_")
                                        or state_key.startswith("new_hire_qty_")
                                    ):
                                        st.session_state.pop(
                                            state_key,
                                            None
                                        )

                                show_order_items_dialog(
                                    selected_quarter_id
                                )


                    st.markdown(
                        """
                        <style>
                        /* 발주/배분 관리 - 발주 버튼 전용 */
                        .st-key-order_action_button [data-testid="stButton"] > button {
                            background: #2e8b57 !important;
                            background-color: #2e8b57 !important;
                            border-color: #2e8b57 !important;
                            color: #ffffff !important;
                            font-weight: 700 !important;
                            font-size: 16px !important;
                        }

                        .st-key-order_action_button [data-testid="stButton"] > button:hover {
                            background: #26734a !important;
                            background-color: #26734a !important;
                            border-color: #26734a !important;
                            color: #ffffff !important;
                        }

                        .st-key-order_action_button [data-testid="stButton"] > button p {
                            color: #ffffff !important;
                            font-weight: 700 !important;
                            font-size: 16px !important;
                            transform: translateY(-1px);
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    # ==================================================
                    # 발주 요약
                    # ==================================================

                    draft_order_result = (
                        admin_supabase
                        .table("orders")
                        .select(
                            "id, quarter_id, distribution_user_count, "
                            "status, ordered_at, memo"
                        )
                        .eq(
                            "quarter_id",
                            selected_quarter_id
                        )
                        .eq(
                            "status",
                            "draft"
                        )
                        .order(
                            "created_at",
                            desc=True
                        )
                        .limit(1)
                        .execute()
                    )

                    total_order_quantity = 0
                    total_order_amount = 0
                    total_per_user_quantity = 0
                    total_per_user_cost = 0
                    order_item_count = 0
                    active_user_count = len(
                        get_registered_users()
                    )

                    if draft_order_result.data:

                        draft_order = (
                            draft_order_result.data[0]
                        )

                        draft_order_id = draft_order["id"]

                        order_items_result = (
                            admin_supabase
                            .table("order_items")
                            .select(
                                "id, item_id, cost_price, "
                                "order_quantity, per_user_quantity, "
                                "memo, received_at, distributed_at"
                            )
                            .eq(
                                "order_id",
                                draft_order_id
                            )
                            .execute()
                        )

                        if order_items_result.data:

                            order_item_count = len(
                                order_items_result.data
                            )

                            for order_item in (
                                order_items_result.data
                            ):

                                cost_price = (
                                    order_item["cost_price"]
                                    or 0
                                )

                                per_user_quantity = (
                                    order_item["per_user_quantity"]
                                    or 0
                                )

                                order_quantity = (
                                    active_user_count
                                    * per_user_quantity
                                )

                                total_per_user_quantity += (
                                    per_user_quantity
                                )

                                total_order_quantity += (
                                    order_quantity
                                )

                                total_per_user_cost += (
                                    cost_price
                                    * per_user_quantity
                                )

                                total_order_amount += (
                                    cost_price
                                    * order_quantity
                                )
                    with st.container(key="order_summary_card"):

                        st.markdown(
                            """
                            <style>
                            .st-key-order_summary_card {
                                background: #ffffff;
                                border: 1px solid #e9ecef;
                                border-radius: 16px;
                                box-shadow: 0 6px 20px rgba(33, 37, 41, 0.08);
                                padding: 20px 20px 18px 20px;
                                margin: 0 0 12px 0;
                                box-sizing: border-box;
                            }

                            .st-key-order_summary_card .order-summary-title {
                                margin: 0 0 16px 0;
                                font-size: 22px;
                                font-weight: 700;
                                line-height: 1.3;
                                color: #212529;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] {
                                gap: 12px;
                                margin-bottom: 12px;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:last-child {
                                margin-bottom: 0;
                            }

                            .st-key-order_summary_card [data-testid="stMetric"] {
                                background: #f8fafb;
                                border: 1px solid #e8edf1;
                                border-radius: 12px;
                                padding: 14px 15px 13px 15px;
                                min-height: 92px;
                                box-sizing: border-box;
                                display: flex;
                                flex-direction: column;
                                justify-content: center;
                            }

                            .st-key-order_summary_card [data-testid="stMetricLabel"] {
                                font-size: 13px;
                                font-weight: 600;
                                color: #6c757d;
                                margin-bottom: 5px;
                            }

                            .st-key-order_summary_card [data-testid="stMetricValue"] {
                                font-size: 26px;
                                font-weight: 700;
                                color: #212529;
                                line-height: 1.2;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {
                                border-top: 3px solid #7aa7e8;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetricValue"] {
                                color: #4169a1;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
                                border-top: 3px solid #83c9a8;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetricValue"] {
                                color: #3d8a64;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {
                                border-top: 3px solid #a99be8;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"] > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetricValue"] {
                                color: #6757a6;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:nth-of-type(2) > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetric"] {
                                border-top: 3px solid #c49ad6;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:nth-of-type(2) > [data-testid="stColumn"]:nth-child(1) [data-testid="stMetricValue"] {
                                color: #8d5c9f;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:nth-of-type(2) > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetric"] {
                                border-top: 3px solid #e7bd73;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:nth-of-type(2) > [data-testid="stColumn"]:nth-child(2) [data-testid="stMetricValue"] {
                                color: #a97822;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:nth-of-type(2) > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetric"] {
                                border-top: 3px solid #79c8c0;
                            }

                            .st-key-order_summary_card [data-testid="stHorizontalBlock"]:nth-of-type(2) > [data-testid="stColumn"]:nth-child(3) [data-testid="stMetricValue"] {
                                color: #3f8e88;
                            }

                            .st-key-order_summary_card [data-testid="stMetricDelta"] {
                                display: none;
                            }
                            </style>
                            """,
                            unsafe_allow_html=True
                        )

                        st.markdown(
                            '<div class="order-summary-title">발주 요약</div>',
                            unsafe_allow_html=True
                        )

                        summary_col1, summary_col2, summary_col3 = st.columns(
                            3
                        )

                        with summary_col1:

                            st.metric(
                                "배분 인원",
                                f"{active_user_count}명"
                            )

                        with summary_col2:

                            st.metric(
                                "품목 종류",
                                f"{order_item_count}종"
                            )

                        with summary_col3:

                            st.metric(
                                "1인당 배분수량",
                                f"{total_per_user_quantity:,}개"
                            )

                        summary_col4, summary_col5, summary_col6 = st.columns(
                            3
                        )

                        with summary_col4:

                            st.metric(
                                "1인당 원가 합계",
                                f"{total_per_user_cost:,.0f}원"
                            )

                        with summary_col5:

                            st.metric(
                                "총 발주수량",
                                f"{total_order_quantity:,}개"
                            )

                        with summary_col6:

                            st.metric(
                                "총 발주금액",
                                f"{total_order_amount:,.0f}원"
                            )

                    st.divider()

        elif menu == "폐기 관리":

            current_quarter = get_current_quarter()

            if not current_quarter:
                st.warning("현재 취합 중인 분기가 없습니다.")
                st.stop()

            active_users = get_registered_users()

            if not active_users:
                st.warning("활성화된 사용자가 없습니다.")
            else:
                user_options = {
                    f"{user['name']} ({user['employee_no']})": user["id"]
                    for user in active_users
                }

                user_options_with_all = {
                    "전체": None,
                    **user_options
                }

                with st.container(key="disposal_top_actions"):
                    top_select_col, top_action_col = st.columns([1, 3])

                    with top_select_col:
                        st.markdown(
                            """
                            <style>
                            .st-key-disposal_top_actions { width: 100% !important; }
                            .st-key-disposal_top_actions [data-testid="stHorizontalBlock"] { align-items: flex-end !important; }
                            .st-key-disposal_top_actions .disposal-user-label {
                                margin: 0 0 6px 0 !important;
                                font-size: 22px !important;
                                font-weight: 700 !important;
                                line-height: 1.35 !important;
                            }
                            .st-key-disposal_top_actions [data-testid="stSelectbox"],
                            .st-key-disposal_top_actions [data-testid="stSelectbox"] > div,
                            .st-key-disposal_top_actions [data-baseweb="select"],
                            .st-key-disposal_top_actions [data-baseweb="select"] > div {
                                width: fit-content !important;
                                min-width: 0 !important;
                            }
                            .st-key-disposal_top_actions [data-baseweb="select"] [role="combobox"],
                            .st-key-disposal_top_actions [data-baseweb="select"] [role="combobox"] *,
                            .st-key-disposal_top_actions [data-baseweb="select"] span {
                                font-size: 16px !important;
                            }
                            .st-key-disposal_top_actions .disposal-action-area [data-testid="stColumn"] {
                                display: flex !important;
                                justify-content: flex-end !important;
                            }
                            .st-key-disposal_top_actions .disposal-action-area [data-testid="stButton"] {
                                width: fit-content !important;
                            }
                            .st-key-disposal_table_header {
                                border-bottom: 1px solid #d9dee5 !important;
                                padding-bottom: 8px !important;
                                margin-bottom: 2px !important;
                            }
                            .st-key-disposal_table_header [data-testid="stColumn"] {
                                display: flex !important;
                                align-items: center !important;
                                justify-content: center !important;
                                text-align: center !important;
                            }
                            .st-key-disposal_table_header [data-testid="stColumn"] p,
                            .st-key-disposal_table_header [data-testid="stColumn"] div {
                                font-weight: 700 !important;
                                text-align: center !important;
                                width: 100% !important;
                            }
                            </style>
                            <div class="disposal-user-label">인원선택</div>
                            """,
                            unsafe_allow_html=True
                        )
                        selected_user_name = st.selectbox(
                            "인원선택",
                            list(user_options_with_all.keys()),
                            index=0,
                            key="admin_disposal_user",
                            label_visibility="collapsed"
                        )

                    button_area = top_action_col.empty()

                selected_user_id = user_options_with_all[
                    selected_user_name
                ]

                disposal_available_result = (
                    admin_supabase
                    .table("quarter_items")
                    .select("item_id")
                    .eq(
                        "quarter_id",
                        current_quarter["id"]
                    )
                    .eq(
                        "disposal_available",
                        True
                    )
                    .execute()
                )

                disposal_available_item_ids = [
                    row["item_id"]
                    for row in disposal_available_result.data
                ]

                disposal_result = (
                    admin_supabase
                    .table("disposals")
                    .select(
                        "id, user_id, item_id, disposed_qty, status, "
                        "approved_by, approved_at, "
                        "inventory_adjusted_at, "
                        "items(product_code, item_name)"
                    )
                    .eq(
                        "quarter_id",
                        current_quarter["id"]
                    )
                    .in_(
                        "item_id",
                        disposal_available_item_ids
                    )
                )

                if selected_user_id is not None:

                    disposal_result = (
                        disposal_result
                        .eq(
                            "user_id",
                            selected_user_id
                        )
                    )

                disposal_result = (
                    disposal_result
                    .order(
                        "created_at",
                        desc=True
                    )
                    .execute()
                )

                if not disposal_result.data:
                    st.info(
                        "폐기 요청 내역이 없습니다."
                    )
                else:
                    if (
                        f"admin_disposal_selected_"
                        f"{selected_user_id}"
                        not in st.session_state
                    ):
                        st.session_state[
                            f"admin_disposal_selected_"
                            f"{selected_user_id}"
                        ] = []

                    selected_disposal_ids = st.session_state[
                        f"admin_disposal_selected_"
                        f"{selected_user_id}"
                    ]

                    def reset_disposal_selection():
                        """폐기관리 액션 실행 후 선택 상태와 체크박스 UI를 함께 초기화."""
                        selected_disposal_ids.clear()
                        st.session_state[
                            f"admin_disposal_selected_"
                            f"{selected_user_id}"
                        ] = selected_disposal_ids

                        for state_key in list(st.session_state.keys()):
                            if state_key.startswith("admin_disposal_select_"):
                                st.session_state[state_key] = False

                    with button_area.container():
                        with st.container(key="disposal_action_area"):
                            # --------------------------------------------------
                            # 선택된 폐기 요청 상태 확인
                            # --------------------------------------------------

                            selected_pending_ids = [
                                disposal_id
                                for disposal_id in selected_disposal_ids
                                if any(
                                    disposal["id"] == disposal_id
                                    and disposal["status"] != "approved"
                                    for disposal in disposal_result.data
                                )
                            ]

                            selected_approved_ids = [
                                disposal_id
                                for disposal_id in selected_disposal_ids
                                if any(
                                    disposal["id"] == disposal_id
                                    and disposal["status"] == "approved"
                                    for disposal in disposal_result.data
                                )
                            ]

                            # --------------------------------------------------
                            # 폐기 작업 버튼
                            # --------------------------------------------------

                            button_col1, button_col2, button_col3 = st.columns(
                                [1.5, 1.5, 1.2]
                            )

                            # --------------------------------------------------
                            # 폐기 확정
                            # --------------------------------------------------

                            with button_col1:

                                if st.button(
                                    "폐기 확정",
                                    type="primary",
                                    key="confirm_disposals"
                                ):

                                    if not selected_pending_ids:

                                        st.warning(
                                            "확정할 미확정 폐기 요청을 선택해주세요."
                                        )
                                        reset_disposal_selection()

                                    else:

                                        for disposal in disposal_result.data:

                                            if (
                                                disposal["id"]
                                                not in selected_pending_ids
                                            ):
                                                continue

                                            disposal_qty = st.session_state.get(
                                                f"admin_disposal_qty_{disposal['id']}",
                                                disposal["disposed_qty"]
                                            )

                                            # 폐기 수량 저장 + 확정
                                            (
                                                admin_supabase
                                                .table("disposals")
                                                .update(
                                                    {
                                                        "disposed_qty": disposal_qty,
                                                        "status": "approved",
                                                        "approved_at": "now()",
                                                        "inventory_adjusted_at": "now()"
                                                    }
                                                )
                                                .eq(
                                                    "id",
                                                    disposal["id"]
                                                )
                                                .execute()
                                            )

                                            # 해당 폐기 요청자의 보유 수량 차감
                                            inventory_result = (
                                                admin_supabase
                                                .table("user_inventory")
                                                .select(
                                                    "id, current_qty"
                                                )
                                                .eq(
                                                    "user_id",
                                                    disposal["user_id"]
                                                )
                                                .eq(
                                                    "item_id",
                                                    disposal["item_id"]
                                                )
                                                .limit(1)
                                                .execute()
                                            )

                                            if inventory_result.data:

                                                inventory = (
                                                    inventory_result.data[0]
                                                )

                                                new_qty = (
                                                    inventory["current_qty"]
                                                    - disposal_qty
                                                )

                                                if new_qty <= 0:

                                                    (
                                                        admin_supabase
                                                        .table("user_inventory")
                                                        .delete()
                                                        .eq(
                                                            "id",
                                                            inventory["id"]
                                                        )
                                                        .execute()
                                                    )

                                                else:

                                                    (
                                                        admin_supabase
                                                        .table("user_inventory")
                                                        .update(
                                                            {
                                                                "current_qty":
                                                                    new_qty
                                                            }
                                                        )
                                                        .eq(
                                                            "id",
                                                            inventory["id"]
                                                        )
                                                        .execute()
                                                    )

                                        reset_disposal_selection()

                                        st.success(
                                            "선택한 폐기 요청이 확정되었습니다."
                                        )

                                        safe_rerun()

                            # --------------------------------------------------
                            # 폐기 확정 취소
                            # --------------------------------------------------

                            with button_col2:

                                if st.button(
                                    "폐기 확정 취소",
                                    key="cancel_disposal_confirmation"
                                ):

                                    if not selected_approved_ids:

                                        st.warning(
                                            "확정 취소할 폐기 요청을 선택해주세요."
                                        )
                                        reset_disposal_selection()

                                    else:

                                        for disposal in disposal_result.data:

                                            if (
                                                disposal["id"]
                                                not in selected_approved_ids
                                            ):
                                                continue

                                            disposal_qty = (
                                                disposal["disposed_qty"]
                                            )

                                            # 해당 폐기 요청자의 보유 수량 복구
                                            inventory_result = (
                                                admin_supabase
                                                .table("user_inventory")
                                                .select(
                                                    "id, current_qty"
                                                )
                                                .eq(
                                                    "user_id",
                                                    disposal["user_id"]
                                                )
                                                .eq(
                                                    "item_id",
                                                    disposal["item_id"]
                                                )
                                                .limit(1)
                                                .execute()
                                            )

                                            if inventory_result.data:

                                                inventory = (
                                                    inventory_result.data[0]
                                                )

                                                restored_qty = (
                                                    inventory["current_qty"]
                                                    + disposal_qty
                                                )

                                                (
                                                    admin_supabase
                                                    .table("user_inventory")
                                                    .update(
                                                        {
                                                            "current_qty":
                                                                restored_qty
                                                        }
                                                    )
                                                    .eq(
                                                        "id",
                                                        inventory["id"]
                                                    )
                                                    .execute()
                                                )

                                            else:

                                                (
                                                    admin_supabase
                                                    .table("user_inventory")
                                                    .insert(
                                                        {
                                                            "user_id":
                                                                disposal["user_id"],
                                                            "item_id":
                                                                disposal["item_id"],
                                                            "current_qty":
                                                                disposal_qty
                                                        }
                                                    )
                                                    .execute()
                                                )

                                            # 폐기 확정 취소
                                            (
                                                admin_supabase
                                                .table("disposals")
                                                .update(
                                                    {
                                                        "status": "pending",
                                                        "approved_at": None,
                                                        "inventory_adjusted_at": None
                                                    }
                                                )
                                                .eq(
                                                    "id",
                                                    disposal["id"]
                                                )
                                                .execute()
                                            )

                                        reset_disposal_selection()

                                        st.success(
                                            "선택한 폐기 확정이 취소되었습니다."
                                        )

                                        safe_rerun()

                            # --------------------------------------------------
                            # 삭제
                            # --------------------------------------------------

                            with button_col3:

                                if st.button(
                                    "삭제",
                                    key="delete_disposals"
                                ):

                                    if not selected_pending_ids:

                                        st.warning(
                                            "삭제할 미확정 폐기 요청을 선택해주세요."
                                        )
                                        reset_disposal_selection()

                                    else:

                                        for disposal_id in selected_pending_ids:

                                            (
                                                admin_supabase
                                                .table("disposals")
                                                .delete()
                                                .eq(
                                                    "id",
                                                    disposal_id
                                                )
                                                .eq(
                                                    "status",
                                                    "pending"
                                                )
                                                .execute()
                                            )

                                        reset_disposal_selection()

                                        st.success(
                                            "선택한 폐기 요청이 삭제되었습니다."
                                        )

                                        safe_rerun()

                st.markdown(
                    """
                    <style>
                    .st-key-disposal_table_header {
                        border-bottom: 1px solid #d9dee5 !important;
                        padding-bottom: 8px !important;
                        margin-bottom: 2px !important;
                    }
                    .st-key-disposal_table_header [data-testid="stColumn"] {
                        display: flex !important;
                        align-items: center !important;
                        justify-content: center !important;
                        text-align: center !important;
                    }
                    .st-key-disposal_table_header [data-testid="stColumn"] p,
                    .st-key-disposal_table_header [data-testid="stColumn"] div {
                        font-weight: 700 !important;
                        text-align: center !important;
                        width: 100% !important;
                    }
                    .st-key-disposal_action_area {
                        width: fit-content !important;
                        max-width: 100% !important;
                        margin-left: auto !important;
                    }
                    .st-key-disposal_action_area [data-testid="stHorizontalBlock"] {
                        width: fit-content !important;
                        margin-left: auto !important;
                        gap: 8px !important;
                    }
                    .st-key-disposal_action_area [data-testid="stColumn"] {
                        width: fit-content !important;
                        min-width: max-content !important;
                        flex: 0 0 auto !important;
                    }
                    .st-key-disposal_action_area [data-testid="stButton"] {
                        width: fit-content !important;
                    }

                    /* 폐기관리 상단 액션 버튼 텍스트만 볼드 처리 */
                    .st-key-disposal_action_area [data-testid="stButton"] button,
                    .st-key-disposal_action_area [data-testid="stButton"] button p,
                    .st-key-disposal_action_area [data-testid="stButton"] button span {
                        font-weight: 700 !important;
                    }

                    /* 폐기 요청 선택 체크박스: 기존처럼 충분한 크기로 중앙 정렬 */
                    [class*="st-key-admin_disposal_select_"] {
                        width: 100% !important;
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                    }
                    [class*="st-key-admin_disposal_select_"] [data-testid="stCheckbox"] {
                        width: 20px !important;
                        min-width: 20px !important;
                        max-width: 20px !important;
                        flex: 0 0 20px !important;
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                        margin: 0 auto !important;
                        padding: 0 !important;
                    }
                    [class*="st-key-admin_disposal_select_"] [data-testid="stCheckbox"] > label {
                        width: 20px !important;
                        min-width: 20px !important;
                        max-width: 20px !important;
                        display: flex !important;
                        justify-content: center !important;
                        align-items: center !important;
                        margin: 0 !important;
                        padding: 0 !important;
                    }
                    [class*="st-key-admin_disposal_select_"] [data-testid="stCheckbox"] > label > div:first-child {
                        width: 20px !important;
                        height: 20px !important;
                        min-width: 20px !important;
                        max-width: 20px !important;
                        min-height: 20px !important;
                        max-height: 20px !important;
                        flex: 0 0 20px !important;
                        margin-left: auto !important;
                        margin-right: auto !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                with st.container(key="disposal_table_header"):
                    if selected_user_id is None:

                        header_col0, header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns(
                            [0.7, 2, 2, 4, 2, 2]
                        )

                        with header_col0:
                            st.write("")

                        with header_col1:
                            st.write("인원")

                        with header_col2:
                            st.write("상품코드")

                        with header_col3:
                            st.write("상품명")

                        with header_col4:
                            st.write("취합수량")

                        with header_col5:
                            st.write("상태")

                    else:

                        header_col0, header_col1, header_col2, header_col3, header_col4 = st.columns(
                            [0.7, 2, 4, 2, 2]
                        )

                        with header_col0:
                            st.write("")

                        with header_col1:
                            st.write("상품코드")

                        with header_col2:
                            st.write("상품명")

                        with header_col3:
                            st.write("취합수량")

                        with header_col4:
                            st.write("상태")

                    st.divider()

                    for disposal in disposal_result.data:

                        item = disposal["items"]

                        if selected_user_id is None:

                            disposal_user = next(
                                (
                                    user
                                    for user in active_users
                                    if user["id"] == disposal["user_id"]
                                ),
                                None
                            )

                            disposal_user_name = (
                                disposal_user["name"]
                                if disposal_user
                                else "-"
                            )

                            col0, col1, col2, col3, col4, col5 = st.columns(
                                [0.7, 2, 2, 4, 2, 2]
                            )

                        else:

                            disposal_user_name = None

                            col0, col1, col2, col3, col4 = st.columns(
                                [0.7, 2, 4, 2, 2]
                            )

                        with col0:

                            if st.checkbox(
                                "선택",
                                key=(
                                    f"admin_disposal_select_"
                                    f"{disposal['id']}"
                                ),
                                label_visibility="collapsed"
                            ):

                                if (
                                    disposal["id"]
                                    not in selected_disposal_ids
                                ):

                                    selected_disposal_ids.append(
                                        disposal["id"]
                                    )

                            else:

                                if (
                                    disposal["id"]
                                    in selected_disposal_ids
                                ):

                                    selected_disposal_ids.remove(
                                        disposal["id"]
                                    )
                        if selected_user_id is None:

                            with col1:
                                st.write(
                                    disposal_user_name
                                )

                            with col2:
                                st.write(
                                    item["product_code"]
                                )

                            with col3:
                                st.write(
                                    item["item_name"]
                                )

                            with col4:
                                st.write(
                                    f"{disposal['disposed_qty']:,}개"
                                )

                            with col5:

                                if disposal["status"] == "approved":

                                    st.write("✓ 확정됨")

                                else:

                                    st.write("미확정")

                        else:

                            with col1:
                                st.write(
                                    item["product_code"]
                                )

                            with col2:
                                st.write(
                                    item["item_name"]
                                )

                            with col3:
                                st.write(
                                    f"{disposal['disposed_qty']:,}개"
                                )

                            with col4:

                                if disposal["status"] == "approved":

                                    st.write("✓ 확정됨")

                                else:

                                    st.write("미확정")

                    selected_disposal_total_qty = sum(
                        int(disposal.get("disposed_qty") or 0)
                        for disposal in disposal_result.data
                        if disposal["id"] in selected_disposal_ids
                    )

                    st.markdown(
                        f"""
                        <style>
                        .disposal-total-area {{
                            width: 100%;
                            box-sizing: border-box;
                            border-top: 1px solid #d9dee5;
                            border-bottom: 1px solid #d9dee5;
                            margin: 0 !important;
                            padding: 8px 0 !important;
                            display: flex;
                            justify-content: flex-end;
                            align-items: center;
                        }}
                        .disposal-total-area .disposal-total-text {{
                            margin: 0 !important;
                            padding: 0 !important;
                            font-size: 20px !important;
                            font-weight: 700 !important;
                            line-height: 1.4;
                            color: #212529;
                            text-align: right;
                        }}
                        </style>
                        <div class="disposal-total-area">
                            <div class="disposal-total-text">총 합계: {selected_disposal_total_qty:,}개</div>
                        </div>
                        """,
                        unsafe_allow_html=True
                    )



        elif menu == "보유수량 조회":

            st.markdown(
                """
                <style>
                /* 보유수량 조회 화면의 실제 콘텐츠 영역만 전체 우측 영역의 2/3로 제한 */
                .st-key-inventory_lookup_header,
                .st-key-inventory_lookup_table {
                    width: 66.6667% !important;
                    max-width: 66.6667% !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            if st.session_state.get("inventory_action_result"):
                show_inventory_action_complete()

            # 보유수량 조회의 users SELECT는 일시적인 HTTPX/Windows
            # 소켓 ReadError가 발생할 수 있으므로 읽기 요청에 한해서만
            # 최대 3회 재시도한다. 데이터 변경 요청에는 적용하지 않는다.
            active_users_result = None
            last_active_users_error = None

            for attempt in range(3):
                try:
                    active_users_result = (
                        admin_supabase
                        .table("users")
                        .select(
                            "id, name, employee_no"
                        )
                        .eq(
                            "is_active",
                            True
                        )
                        .order(
                            "name",
                            desc=False
                        )
                        .execute()
                    )
                    break

                except (
                    httpx.ReadError,
                    httpx.ConnectError,
                    httpx.ConnectTimeout,
                    httpx.ReadTimeout,
                ) as e:
                    last_active_users_error = e

                    if attempt < 2:
                        time.sleep(0.8 * (2 ** attempt))

            if active_users_result is None:
                raise last_active_users_error

            user_options = {
                f"{user['name']}({user['employee_no']})": user["id"]
                for user in active_users_result.data
            }

            with st.container(key="inventory_lookup_header"):

                st.markdown(
                    """
                    <style>
                    .st-key-inventory_lookup_header .inventory-lookup-label {
                        font-size: 20px !important;
                        font-weight: 700 !important;
                        line-height: 1.4 !important;
                        margin-bottom: 6px !important;
                    }
                    .st-key-inventory_lookup_header [data-testid="stSelectbox"] {
                        width: fit-content !important;
                        min-width: 0 !important;
                    }
                    .st-key-inventory_lookup_header [data-baseweb="select"] {
                        width: fit-content !important;
                        min-width: 0 !important;
                    }
                    .st-key-inventory_lookup_header [data-baseweb="select"] > div {
                        width: fit-content !important;
                        min-width: 0 !important;
                    }
                    .st-key-inventory_lookup_header [data-baseweb="select"] [role="combobox"] {
                        width: fit-content !important;
                        min-width: 0 !important;
                    }
                    .st-key-inventory_lookup_header [data-baseweb="select"] * {
                        white-space: nowrap !important;
                    }
                    </style>
                    <div class="inventory-lookup-label">조회할 인원</div>
                    """,
                    unsafe_allow_html=True
                )

                selected_user_name = st.selectbox(
                    "조회할 인원",
                    list(user_options.keys()),
                    key="inventory_admin_user",
                    label_visibility="collapsed"
                )

            selected_user_id = (
                user_options[
                    selected_user_name
                ]
            )

            inventory_result = (
                admin_supabase
                .table("user_inventory")
                .select(
                    "id, item_id, current_qty, "
                    "items(store_name, product_code, item_name, category_id)"
                )
                .eq(
                    "user_id",
                    selected_user_id
                )
                .gt(
                    "current_qty",
                    0
                )
                .order(
                    "updated_at",
                    desc=True
                )
                .execute()
            )

            with st.container(key="inventory_lookup_table"):

                st.markdown(
                    """
                    <style>
                    .st-key-inventory_lookup_table .inventory-table-header,
                    .st-key-inventory_lookup_table .inventory-table-cell {
                        display: flex;
                        align-items: center;
                        min-height: 38px;
                        box-sizing: border-box;
                    }
                    .st-key-inventory_lookup_table .inventory-table-header {
                        font-weight: 700;
                        text-align: center !important;
                        justify-content: center !important;
                        align-items: center !important;
                        width: 100%;
                    }
                    .st-key-inventory_lookup_table .stButton {
                        width: 100% !important;
                    }
                    .st-key-inventory_lookup_table .stButton > button {
                        width: 100% !important;
                        min-height: 38px !important;
                        padding: 6px 4px !important;
                        border: 1px solid transparent !important;
                        background: transparent !important;
                        color: inherit !important;
                        box-shadow: none !important;
                        justify-content: center !important;
                        text-align: center !important;
                    }
                    .st-key-inventory_lookup_table .stButton > button:hover {
                        border-color: #d9d9d9 !important;
                        background: #f7f8fa !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                if not inventory_result.data:

                    st.info(
                        "현재 보유하고 있는 상품이 없습니다."
                    )

                else:

                    header_col1, header_col2, header_col3 = st.columns(
                        [2, 4, 1]
                    )

                    with header_col1:
                        st.markdown(
                            '<div class="inventory-table-header">상품코드</div>',
                            unsafe_allow_html=True
                        )

                    with header_col2:
                        st.markdown(
                            '<div class="inventory-table-header">상품명</div>',
                            unsafe_allow_html=True
                        )

                    with header_col3:
                        st.markdown(
                            '<div class="inventory-table-header">수량</div>',
                            unsafe_allow_html=True
                        )

                    st.markdown(
                        '<hr style="margin: 0.225rem 0 1rem 0; border: none; border-top: 1px solid #d9d9d9;">',
                        unsafe_allow_html=True
                    )

                    for inventory in inventory_result.data:

                        item = inventory.get("items")

                        if not item:
                            continue

                        inventory_id = inventory["id"]
                        item_name = item["item_name"]
                        product_code = item["product_code"]
                        current_qty = inventory["current_qty"]

                        col1, col2, col3 = st.columns(
                            [2, 4, 1]
                        )

                        with col1:
                            if st.button(
                                product_code,
                                key=f"inventory_row_code_{inventory_id}",
                                use_container_width=True
                            ):
                                show_edit_inventory_dialog(
                                    inventory_id,
                                    item_name,
                                    product_code,
                                    current_qty
                                )

                        with col2:
                            if st.button(
                                item_name,
                                key=f"inventory_row_name_{inventory_id}",
                                use_container_width=True
                            ):
                                show_edit_inventory_dialog(
                                    inventory_id,
                                    item_name,
                                    product_code,
                                    current_qty
                                )

                        with col3:
                            if st.button(
                                f"{current_qty:,}개",
                                key=f"inventory_row_qty_{inventory_id}",
                                use_container_width=True
                            ):
                                show_edit_inventory_dialog(
                                    inventory_id,
                                    item_name,
                                    product_code,
                                    current_qty
                                )

            
        elif menu == "처리내역":

            quarters_data = get_all_quarters()

            if not quarters_data:
                st.info("등록된 분기가 없습니다.")
                st.stop()

            st.markdown(
                """
                <style>
                .st-key-processing_main_grid {
                    margin-left: -1rem !important;
                    width: calc(100% + 1rem) !important;
                }

                .st-key-processing_main_grid > div[data-testid="stHorizontalBlock"] > div[data-testid="column"] {
                    transform: translateY(-55px) !important;
                }
                </style>
                """,
                unsafe_allow_html=True
            )

            with st.container(key="processing_main_grid"):

                processing_left, processing_right = st.columns(
                    [1, 1],
                    gap="large"
                )

            with processing_left:

                st.markdown(
                    """
                    <style>
                    .st-key-processing_distribution_panel [data-testid="stSelectbox"] > label {
                        font-weight: 700 !important;
                    }
                    .st-key-processing_distribution_panel [data-testid="stSelectbox"] {
                        width: fit-content !important;
                        max-width: fit-content !important;
                    }
                    .st-key-processing_distribution_panel [data-testid="stSelectbox"] > div {
                        width: fit-content !important;
                        max-width: fit-content !important;
                    }
                    .st-key-processing_distribution_panel [data-testid="stSelectbox"] [data-baseweb="select"],
                    .st-key-processing_distribution_panel [data-testid="stSelectbox"] [data-baseweb="select"] > div {
                        width: fit-content !important;
                        min-width: fit-content !important;
                        max-width: fit-content !important;
                    }
                    .st-key-processing_distribution_panel .processing-product-name {
                        white-space: normal !important;
                        overflow-wrap: break-word !important;
                        word-wrap: break-word !important;
                        word-break: break-all !important;
                    }
                    .st-key-processing_distribution_panel .processing-header-text {
                        font-weight: 700 !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                with st.container(key="processing_distribution_panel"):

                    st.subheader("배분내역 조회")


                    (
                        selected_distribution_major,
                        selected_distribution_detail,
                        selected_quarter_id,
                        selected_distribution_batch_id
                    ) = render_hierarchical_quarter_selector(
                        quarters_data,
                        label="분기 선택",
                        major_key="transaction_distribution_major",
                        detail_key="transaction_distribution_detail",
                        include_new_hire=True,
                        include_all=True
                    )

                    # -----------------------------------------------------
                    # 실제 배분 이력 조회
                    # -----------------------------------------------------
                    # 보유수량 반영과 별개로 기록되는 distribution_history를
                    # 처리내역의 기준 데이터로 사용합니다.
                    distribution_summary = get_distribution_history_summary(
                        selected_quarter_id,
                        selected_distribution_batch_id
                    )

                    def render_distribution_rows(summary_rows):

                        if not summary_rows:
                            return False

                        def distribution_sort_key(row):
                            quarter_label = str(
                                row.get(
                                    "quarter_label",
                                    ""
                                )
                            )

                            quarter_match = re.search(
                                r"(20\d{2})\s*년\s*([1-4])\s*분기",
                                quarter_label
                            )

                            if quarter_match:
                                year = int(
                                    quarter_match.group(1)
                                )
                                quarter = int(
                                    quarter_match.group(2)
                                )
                            else:
                                year = -1
                                quarter = -1

                            return (
                                -year,
                                -quarter,
                                row["item"].get(
                                    "product_code",
                                    ""
                                )
                            )

                        sorted_rows = sorted(
                            summary_rows,
                            key=distribution_sort_key
                        )

                        header_col1, header_col2, header_col3, header_col4, header_col5 = st.columns(
                            [2, 4, 2, 2, 2]
                        )

                        with header_col1:
                            st.markdown(
                                "<div class=\"processing-header-text\">상품코드</div>",
                                unsafe_allow_html=True
                            )

                        with header_col2:
                            st.markdown(
                                "<div class=\"processing-header-text\">상품명</div>",
                                unsafe_allow_html=True
                            )

                        with header_col3:
                            st.markdown(
                                "<div class=\"processing-header-text\">1인당 배분</div>",
                                unsafe_allow_html=True
                            )

                        with header_col4:
                            st.markdown(
                                "<div class=\"processing-header-text\">배분 인원</div>",
                                unsafe_allow_html=True
                            )

                        with header_col5:
                            st.markdown(
                                "<div class=\"processing-header-text\">배분 분기</div>",
                                unsafe_allow_html=True
                            )

                        st.divider()

                        active_detail_key = st.session_state.get(
                            "transaction_distribution_user_detail"
                        )

                        for row in sorted_rows:

                            item = row["item"]
                            row_detail_key = (
                                f"{row.get('quarter_id')}_"
                                f"{row.get('item_id')}"
                            )

                            col1, col2, col3, col4, col5 = st.columns(
                                [2, 4, 2, 2, 2]
                            )

                            with col1:
                                st.write(
                                    item["product_code"]
                                )

                            with col2:
                                st.markdown(
                                    f'<div class="processing-product-name">{item["item_name"]}</div>',
                                    unsafe_allow_html=True
                                )

                            with col3:
                                st.write(
                                    row.get(
                                        "per_user_quantity_text",
                                        "0개"
                                    )
                                )

                            with col4:
                                if st.button(
                                    f"{len(row['user_ids']):,}명",
                                    key=(
                                        "transaction_distribution_users_"
                                        f"{row_detail_key}"
                                    ),
                                    width="content",
                                    type="tertiary"
                                ):
                                    if active_detail_key == row_detail_key:
                                        st.session_state.pop(
                                            "transaction_distribution_user_detail",
                                            None
                                        )
                                    else:
                                        st.session_state[
                                            "transaction_distribution_user_detail"
                                        ] = row_detail_key

                                    active_detail_key = st.session_state.get(
                                        "transaction_distribution_user_detail"
                                    )

                            with col5:
                                st.write(
                                    row.get(
                                        "quarter_label",
                                        "분기 미상"
                                    )
                                )

                            if active_detail_key == row_detail_key:

                                users_map = get_users_by_ids(
                                    list(row["user_quantities"].keys())
                                )

                                st.caption("배분된 인원")

                                user_rows = []

                                for user_id, quantity in row[
                                    "user_quantities"
                                ].items():
                                    user = users_map.get(
                                        str(user_id),
                                        {}
                                    )

                                    user_rows.append(
                                        (
                                            str(
                                                user.get(
                                                    "name",
                                                    "알 수 없는 사용자"
                                                )
                                            ),
                                            str(
                                                user.get(
                                                    "employee_no",
                                                    "-"
                                                )
                                            ),
                                            int(quantity)
                                        )
                                    )

                                user_rows.sort(
                                    key=lambda value: (
                                        value[0],
                                        value[1]
                                    )
                                )

                                if user_rows:
                                    for (
                                        user_name,
                                        employee_no,
                                        quantity
                                    ) in user_rows:
                                        st.write(
                                            f"• {user_name} "
                                            f"({employee_no}) "
                                            f"— {quantity:,}개"
                                        )
                                else:
                                    st.caption(
                                        "배분된 인원 정보가 없습니다."
                                    )

                                st.divider()

                        st.divider()
                        return True

                    if selected_distribution_batch_id is not None:

                        selected_rows = list(
                            distribution_summary.values()
                        )

                        if not selected_rows:
                            st.info("선택한 신규입사 배분 내역이 없습니다.")
                        else:
                            st.markdown(
                                f"**신규입사 · {selected_distribution_detail}**"
                            )
                            render_distribution_rows(selected_rows)

                    elif selected_quarter_id is None:

                        selected_rows = list(
                            distribution_summary.values()
                        )

                        if not selected_rows:
                            st.info("배분된 내역이 없습니다.")
                        else:
                            # 전체 조회에서는 별도의 분기 제목을 반복해서 출력하지 않고
                            # 각 행의 "배분 분기" 열로 분기를 명확하게 표시합니다.
                            render_distribution_rows(
                                selected_rows
                            )

                    else:

                        selected_rows = [
                            row
                            for row in distribution_summary.values()
                            if row["quarter_id"] == selected_quarter_id
                        ]

                        if not selected_rows:
                            st.info(
                                "아직 배분된 내역이 없습니다."
                            )
                        else:
                            render_distribution_rows(
                                selected_rows
                            )

            with processing_right:

                st.markdown(
                    """
                    <style>
                    .st-key-processing_disposal_panel [data-testid="stSelectbox"] > label {
                        font-weight: 700 !important;
                    }
                    .st-key-processing_disposal_panel [data-testid="stSelectbox"] {
                        width: fit-content !important;
                        max-width: fit-content !important;
                    }
                    .st-key-processing_disposal_panel [data-testid="stSelectbox"] > div {
                        width: fit-content !important;
                        max-width: fit-content !important;
                    }
                    .st-key-processing_disposal_panel [data-testid="stSelectbox"] [data-baseweb="select"],
                    .st-key-processing_disposal_panel [data-testid="stSelectbox"] [data-baseweb="select"] > div {
                        width: fit-content !important;
                        min-width: fit-content !important;
                        max-width: fit-content !important;
                    }
                    .st-key-processing_disposal_panel .processing-header-text {
                        font-weight: 700 !important;
                    }
                    </style>
                    """,
                    unsafe_allow_html=True
                )

                with st.container(key="processing_disposal_panel"):

                    st.subheader("폐기내역 조회")


                    # 분기 / 대분류 / 세부분류 / 인원선택을
                    # 하나의 필터 영역에서만 렌더링합니다.
                    # 기존 중복 위젯은 제거하여 동일한 key가
                    # 두 번 생성되지 않도록 합니다.

                    # -----------------------------------------------------
                    # 폐기내역 조회 필터
                    # 대분류 / 세부분류 / 인원선택을 한 줄에 배치
                    # -----------------------------------------------------
                    majors, major_details, detail_map = build_hierarchical_quarter_options(
                        quarters_data,
                        include_new_hire=False,
                        include_all=True
                    )

                    selector_container_key = "processing_disposal_filter_row"

                    st.markdown(
                        """
                        <style>
                        .st-key-processing_disposal_filter_row {
                            width: 100% !important;
                        }
                        .st-key-processing_disposal_filter_row [data-testid="stSelectbox"] {
                            width: 100% !important;
                        }
                        .st-key-processing_disposal_filter_row [data-testid="stSelectbox"] > div,
                        .st-key-processing_disposal_filter_row [data-baseweb="select"],
                        .st-key-processing_disposal_filter_row [data-baseweb="select"] > div {
                            width: 100% !important;
                        }
                        .st-key-processing_disposal_filter_row [data-testid="stSelectbox"] label {
                            font-weight: 700 !important;
                        }
                        </style>
                        """,
                        unsafe_allow_html=True
                    )

                    current_disposal_major = st.session_state.get(
                        "transaction_disposal_major"
                    )
                    if current_disposal_major not in majors:
                        current_disposal_major = majors[0]

                    with st.container(key=selector_container_key):
                        st.caption("분기 선택")

                        filter_col1, filter_col2, filter_col3 = st.columns(
                            [1, 1, 1],
                            gap="small"
                        )

                        with filter_col1:
                            selected_disposal_major = st.selectbox(
                                "대분류",
                                majors,
                                index=majors.index(current_disposal_major),
                                key="transaction_disposal_major"
                            )

                        disposal_detail_options = major_details.get(
                            selected_disposal_major,
                            []
                        )

                        current_disposal_detail = st.session_state.get(
                            "transaction_disposal_detail"
                        )
                        if current_disposal_detail not in disposal_detail_options:
                            current_disposal_detail = (
                                disposal_detail_options[0]
                                if disposal_detail_options
                                else None
                            )

                        with filter_col2:
                            selected_disposal_detail = st.selectbox(
                                "세부 분류",
                                disposal_detail_options,
                                index=(
                                    disposal_detail_options.index(
                                        current_disposal_detail
                                    )
                                    if current_disposal_detail in disposal_detail_options
                                    else 0
                                ),
                                key="transaction_disposal_detail"
                            )

                        active_users = get_registered_users()

                        user_options = {
                            "전체": None
                        }

                        for user in active_users:
                            user_options[user["name"]] = user["id"]

                        with filter_col3:
                            selected_user_name = st.selectbox(
                                "인원 선택",
                                list(user_options.keys()),
                                key="transaction_disposal_user"
                            )

                        selected_user_id = user_options[
                            selected_user_name
                        ]

                    selected_disposal_target = detail_map.get(
                        (
                            selected_disposal_major,
                            selected_disposal_detail
                        ),
                        {}
                    )

                    selected_quarter_id = selected_disposal_target.get(
                        "quarter_id"
                    )

                    # -----------------------------------------------------
                    # 폐기내역 공통 렌더링
                    # 헤더는 항상 이름 / 상품코드 / 상품명 / 폐기수량 고정
                    # -----------------------------------------------------
                    disposal_display_rows = []

                    def append_disposal_rows(
                        disposal_rows,
                        user_name
                    ):
                        for disposal in disposal_rows or []:
                            item = disposal.get("items")

                            if not item:
                                continue

                            disposal_display_rows.append(
                                {
                                    "user_name": user_name,
                                    "product_code": item.get(
                                        "product_code",
                                        ""
                                    ),
                                    "item_name": item.get(
                                        "item_name",
                                        ""
                                    ),
                                    "disposed_qty": disposal.get(
                                        "disposed_qty",
                                        0
                                    )
                                }
                            )

                    # -----------------------------------------------------
                    # 폐기 - 특정 분기 / 특정 인원
                    # -----------------------------------------------------
                    if (
                        selected_quarter_id is not None
                        and selected_user_id is not None
                    ):

                        disposal_result = (
                            admin_supabase
                            .table("disposals")
                            .select(
                                "disposed_qty, status, "
                                "items(product_code, item_name)"
                            )
                            .eq(
                                "quarter_id",
                                selected_quarter_id
                            )
                            .eq(
                                "user_id",
                                selected_user_id
                            )
                            .eq(
                                "status",
                                "approved"
                            )
                            .execute()
                        )

                        append_disposal_rows(
                            disposal_result.data,
                            selected_user_name
                        )

                    # -----------------------------------------------------
                    # 폐기 - 특정 분기 / 전체 인원
                    # -----------------------------------------------------
                    elif (
                        selected_quarter_id is not None
                        and selected_user_id is None
                    ):

                        for user in active_users:

                            disposal_result = (
                                admin_supabase
                                .table("disposals")
                                .select(
                                    "disposed_qty, status, "
                                    "items(product_code, item_name)"
                                )
                                .eq(
                                    "quarter_id",
                                    selected_quarter_id
                                )
                                .eq(
                                    "user_id",
                                    user["id"]
                                )
                                .eq(
                                    "status",
                                    "approved"
                                )
                                .execute()
                            )

                            append_disposal_rows(
                                disposal_result.data,
                                user["name"]
                            )

                    # -----------------------------------------------------
                    # 폐기 - 전체 분기 / 특정 인원
                    # -----------------------------------------------------
                    elif (
                        selected_quarter_id is None
                        and selected_user_id is not None
                    ):

                        for quarter in quarters_data:

                            disposal_result = (
                                admin_supabase
                                .table("disposals")
                                .select(
                                    "disposed_qty, status, "
                                    "items(product_code, item_name)"
                                )
                                .eq(
                                    "quarter_id",
                                    quarter["id"]
                                )
                                .eq(
                                    "user_id",
                                    selected_user_id
                                )
                                .eq(
                                    "status",
                                    "approved"
                                )
                                .execute()
                            )

                            append_disposal_rows(
                                disposal_result.data,
                                selected_user_name
                            )

                    # -----------------------------------------------------
                    # 폐기 - 전체 분기 / 전체 인원
                    # -----------------------------------------------------
                    else:

                        for quarter in quarters_data:

                            for user in active_users:

                                disposal_result = (
                                    admin_supabase
                                    .table("disposals")
                                    .select(
                                        "disposed_qty, status, "
                                        "items(product_code, item_name)"
                                    )
                                    .eq(
                                        "quarter_id",
                                        quarter["id"]
                                    )
                                    .eq(
                                        "user_id",
                                        user["id"]
                                    )
                                    .eq(
                                        "status",
                                        "approved"
                                    )
                                    .execute()
                                )

                                append_disposal_rows(
                                    disposal_result.data,
                                    user["name"]
                                )

                    if not disposal_display_rows:

                        if (
                            selected_quarter_id is not None
                            and selected_user_id is not None
                        ):
                            st.info(
                                "해당 인원의 확정된 폐기 내역이 없습니다."
                            )
                        elif (
                            selected_quarter_id is not None
                            and selected_user_id is None
                        ):
                            st.info(
                                "해당 분기에 폐기된 내역이 없습니다."
                            )
                        elif (
                            selected_quarter_id is None
                            and selected_user_id is not None
                        ):
                            st.info(
                                "해당 인원의 확정된 폐기 내역이 없습니다."
                            )
                        else:
                            st.info(
                                "폐기된 내역이 없습니다."
                            )

                    else:

                        disposal_display_rows.sort(
                            key=lambda row: (
                                str(row.get("user_name") or "").strip().casefold(),
                                str(row.get("product_code") or "").strip(),
                                str(row.get("item_name") or "").strip().casefold()
                            )
                        )

                        header_col1, header_col2, header_col3, header_col4 = st.columns(
                            [2.2, 2.2, 4.6, 1.5]
                        )

                        with header_col1:
                            st.markdown(
                                "<div class=\"processing-header-text\">이름</div>",
                                unsafe_allow_html=True
                            )

                        with header_col2:
                            st.markdown(
                                "<div class=\"processing-header-text\">상품코드</div>",
                                unsafe_allow_html=True
                            )

                        with header_col3:
                            st.markdown(
                                "<div class=\"processing-header-text\">상품명</div>",
                                unsafe_allow_html=True
                            )

                        with header_col4:
                            st.markdown(
                                "<div class=\"processing-header-text\">폐기수량</div>",
                                unsafe_allow_html=True
                            )

                        st.divider()

                        for row in disposal_display_rows:

                            col1, col2, col3, col4 = st.columns(
                                [2.2, 2.2, 4.6, 1.5]
                            )

                            with col1:
                                st.write(row["user_name"])

                            with col2:
                                st.write(row["product_code"])

                            with col3:
                                st.markdown(
                                    f'<div class="processing-product-name">{row["item_name"]}</div>',
                                    unsafe_allow_html=True
                                )

                            with col4:
                                st.write(
                                    f"-{int(row['disposed_qty']):,}개"
                                )

if (
    st.session_state.get("show_user_collection")
    and st.session_state.get("login_mode") == "user"
):

    # 사용자 이름
    st.markdown(
        f"""
        <div style="
            font-size: 20px;
            font-weight: 700;
            margin-bottom: 14px;
        ">
            {st.session_state.get('collection_identified_name', '')}님, 반갑습니다.
        </div>
        """,
        unsafe_allow_html=True
    )

    # 로그아웃
    if st.button(
        "로그아웃",
        key="user_logout",
        type="tertiary",
        width="content"
    ):

        st.session_state.logged_in = False
        st.session_state.login_mode = None
        st.session_state.admin_login = False
        st.session_state.show_user_collection = False
        st.session_state.collection_user_id = None
        st.session_state.collection_identified_name = None
        st.session_state.distribution_selected_items = []
        st.session_state.distribution_loaded_key = None
        st.session_state.user_notice_dismissed = False
        st.session_state.selected_disposal_items = []
        st.session_state.disposal_loaded_key = None

        safe_rerun()

    st.markdown(
        """
        <style>
        div[data-testid="stColumn"]:has(button[key="user_mode_distribution"]) button,
        div[data-testid="stColumn"]:has(button[key="user_mode_disposal"]) button,
        div[data-testid="stColumn"]:has(button[key="user_menu_inventory"]) button {
            background: transparent !important;
            border: none !important;
            box-shadow: none !important;
            color: inherit !important;
            justify-content: flex-start !important;
            padding-left: 0 !important;
            font-size: 20px !important;
            font-weight: 400 !important;
        }

        div[data-testid="stColumn"]:has(button[key="user_mode_distribution"]) button:hover,
        div[data-testid="stColumn"]:has(button[key="user_mode_disposal"]) button:hover,
        div[data-testid="stColumn"]:has(button[key="user_menu_inventory"]) button:hover {
            color: #ff4b4b !important;
        }

        div[data-testid="stColumn"]:has(button[key="user_mode_distribution"]),
        div[data-testid="stColumn"]:has(button[key="user_mode_disposal"]),
        div[data-testid="stColumn"]:has(button[key="user_menu_inventory"]) {
            margin-left: -18px !important;
        }

        div[data-testid="stColumn"]:has(select[aria-label=""]) {
            font-size: 18px !important;
        }

        div[data-testid="stColumn"]:has(select[aria-label=""]) [data-baseweb="select"] {
            font-size: 18px !important;
        }

        div[role="option"] {
            font-size: 18px !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        /* 사용자 페이지 전체 고정 레이아웃 */
        html,
        body {
            min-width: 1600px !important;
            overflow-x: auto !important;
        }

        [data-testid="stAppViewContainer"] {
            min-width: 1600px !important;
        }

        [data-testid="stAppViewContainer"] .main .block-container {
            width: 1600px !important;
            min-width: 1600px !important;
            max-width: 1600px !important;
            margin-left: 0 !important;
            margin-right: 0 !important;
        }

        [data-testid="stHorizontalBlock"] {
            flex-wrap: nowrap !important;
        }

        [data-testid="stColumn"] {
            min-width: 0 !important;
        }

        [data-testid="stColumn"] button,
        [data-testid="stColumn"] p,
        [data-testid="stColumn"] span,
        [data-testid="stColumn"] label {
            white-space: nowrap !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    st.markdown(
        """
        <style>
        /* 요청 목록 컨테이너만 초록색으로 표시 */
        [class*="st-key-request_panel_distribution"],
        [class*="st-key-request_panel_disposal"] {
            background: #e4f7e9 !important;
            border: none !important;
            border-radius: 16px !important;
            padding: 16px !important;
            box-shadow: none !important;
        }

        [class*="st-key-request_panel_distribution"] > div,
        [class*="st-key-request_panel_disposal"] > div {
            background: #e4f7e9 !important;
            border-radius: 13px !important;
        }

        /* 배분 요청 목록 행 간격을 균일하게 정리 */
        [class*="st-key-request_panel_distribution"] [data-testid="stHorizontalBlock"] {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            min-height: 32px !important;
            align-items: center !important;
        }

        [class*="st-key-request_panel_distribution"] [data-testid="stHorizontalBlock"] p {
            margin-top: 0 !important;
            margin-bottom: 0 !important;
            padding-top: 0 !important;
            padding-bottom: 0 !important;
            line-height: 32px !important;
        }

        [class*="st-key-request_panel_distribution"] hr,
        [class*="st-key-request_panel_disposal"] hr {
            border-color: #2e8b57 !important;
        }

        /* 요청 목록 삭제 버튼 */
        [class*="st-key-remove_collection_"] button,
        [class*="st-key-remove_disposal_"] button {
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            min-height: 32px !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 50% !important;
            background: #2e8b57 !important;
            border: none !important;
            box-shadow: none !important;
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        [class*="st-key-remove_collection_"] button p,
        [class*="st-key-remove_disposal_"] button p {
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transform: translateY(-1px) !important;
        }

        [class*="st-key-remove_collection_"] button:hover,
        [class*="st-key-remove_disposal_"] button:hover,
        [class*="st-key-add_collection_"] button:hover,
        [class*="st-key-add_disposal_"] button:hover {
            background: #26734a !important;
            border: none !important;
        }

        /* 상품 카드 추가 버튼 - 삭제 버튼과 동일한 원형 디자인 */
        [class*="st-key-add_collection_"] button,
        [class*="st-key-add_disposal_"] button {
            width: 32px !important;
            height: 32px !important;
            min-width: 32px !important;
            min-height: 32px !important;
            padding: 0 !important;
            margin: 0 !important;
            border-radius: 50% !important;
            background: #2e8b57 !important;
            border: none !important;
            box-shadow: none !important;
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
        }

        [class*="st-key-add_collection_"] button p,
        [class*="st-key-add_disposal_"] button p {
            color: #ffffff !important;
            font-size: 20px !important;
            font-weight: 900 !important;
            line-height: 1 !important;
            margin: 0 !important;
            padding: 0 !important;
            display: flex !important;
            align-items: center !important;
            justify-content: center !important;
            transform: translateY(-1px) !important;
        }
        </style>
        """,
        unsafe_allow_html=True
    )

    user_menu_area, user_content_area, user_request_area = st.columns(
        [1, 5, 3],
        gap="large"
    )

    with user_menu_area:

        st.markdown(
            """
            <div style="
                font-size: 20px;
                font-weight: 700;
                margin-bottom: 12px;
            ">
                사용자 메뉴
            </div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "배분",
            key="user_mode_distribution",
            type="tertiary",
            width="content"
        ):

            st.session_state.user_collection_mode = "배분"
            st.session_state.user_menu = "배분/폐기"
            reset_menu_transition_state()

        if st.button(
            "폐기",
            key="user_mode_disposal",
            type="tertiary",
            width="content"
        ):

            st.session_state.user_collection_mode = "폐기"
            st.session_state.user_menu = "배분/폐기"
            reset_menu_transition_state()

        st.markdown(
            """
            <div style="height: 4px;"></div>
            """,
            unsafe_allow_html=True
        )

        if st.button(
            "보유수량 조회",
            key="user_menu_inventory",
            type="tertiary",
            width="content"
        ):

            st.session_state.user_menu = "보유수량 조회"
            reset_menu_transition_state()

    user_menu = st.session_state.get(
        "user_menu",
        "배분/폐기"
    )

    collection_mode = st.session_state.get(
        "user_collection_mode",
        "배분"
    )

    with user_content_area:

        if user_menu == "보유수량 조회":

            st.subheader("보유수량 조회")

            inventory_result = (
                admin_supabase
                .table("user_inventory")
                .select(
                    "current_qty, "
                    "items(product_code, item_name)"
                )
                .eq(
                    "user_id",
                    st.session_state.collection_user_id
                )
                .gt(
                    "current_qty",
                    0
                )
                .execute()
            )

            inventory_rows = sorted(
                inventory_result.data or [],
                key=lambda row: str(
                    (row.get("items") or {}).get("item_name", "")
                )
            )

            if inventory_rows:

                header_col1, header_col2, header_col3 = st.columns(
                    [2, 4, 1]
                )

                with header_col1:
                    st.markdown("**상품코드**")

                with header_col2:
                    st.markdown("**상품명**")

                with header_col3:
                    st.markdown("**수량**")

                st.markdown(
                    "<hr style=\"margin: 0.15rem 0 0.5rem 0; border: none; border-top: 1px solid #d9d9d9;\">",
                    unsafe_allow_html=True
                )

                for row in inventory_rows:

                    item = row.get("items")

                    if not item:
                        continue

                    col1, col2, col3 = st.columns(
                        [2, 4, 1]
                    )

                    with col1:
                        st.write(
                            item["product_code"]
                        )

                    with col2:
                        st.write(
                            item["item_name"]
                        )

                    with col3:
                        st.write(
                            f"{row['current_qty']}개"
                        )

            else:

                st.info(
                    "현재 보유한 품목이 없습니다."
                )

            st.stop()


    # ============================================================
    # 사용자 취합 / 폐기
    # ============================================================

    quarter_result = (
        admin_supabase
        .table("quarters")
        .select(
            "id, year, quarter, start_date, end_date, status"
        )
        .eq(
            "status",
            "collecting"
        )
        .order(
            "year",
            desc=True
        )
        .order(
            "quarter",
            desc=True
        )
        .limit(1)
        .execute()
    )

    if not quarter_result.data:

        if not st.session_state.get(
            "user_notice_dismissed",
            False
        ):
            show_user_notice(
                "현재 취합 가능한 분기가 없습니다."
            )

    else:

        current_quarter = quarter_result.data[0]

        today = date.today()
        end_date = date.fromisoformat(
            current_quarter["end_date"]
        )

        collection_closed = today > end_date

        # ========================================================
        # 마감 후
        # ========================================================

        if collection_closed:

            if not st.session_state.get(
                "user_notice_dismissed",
                False
            ):

                show_user_notice(
                    "취합 마감일이 지나 취합이 종료되었습니다."
                )

            with user_content_area:

                closed_request_col, closed_divider_col, closed_disposal_col = st.columns(
                    [1, 0.015, 1],
                    gap="large"
                )

                with closed_divider_col:
                    st.markdown(
                        """
                        <div style="
                            height: 150px;
                            border-left: 1px solid #d9d9d9;
                            margin-top: 4px;
                        "></div>
                        """,
                        unsafe_allow_html=True
                    )

                with closed_request_col:

                    # ----------------------------------------------------
                    # 기존 취합 요청 목록
                    # ----------------------------------------------------

                    st.subheader(
                        "취합 요청 목록"
                    )

                    saved_requests_result = (
                        admin_supabase
                        .table("requests")
                        .select(
                            "item_id, requested_qty, "
                            "items(item_name, product_code)"
                        )
                        .eq(
                            "user_id",
                            st.session_state.collection_user_id
                        )
                        .eq(
                            "quarter_id",
                            current_quarter["id"]
                        )
                        .execute()
                    )

                    if saved_requests_result.data:

                        for row in saved_requests_result.data:

                            item_info = row.get("items")

                            if not item_info:
                                continue

                            col1, col2, col3 = st.columns(
                                [2, 5, 1]
                            )

                            with col1:
                                st.write(
                                    item_info["product_code"]
                                )

                            with col2:
                                st.write(
                                    item_info["item_name"]
                                )

                            with col3:
                                st.write(
                                    f"{row['requested_qty']}개"
                                )

                    else:

                        st.write(
                            "취합 요청 내역이 없습니다."
                        )

                with closed_disposal_col:

                    # ----------------------------------------------------
                    # 기존 폐기 요청 목록
                    # ----------------------------------------------------

                    st.subheader(
                        "폐기 요청 목록"
                    )

                    saved_disposals_result = (
                        admin_supabase
                        .table("disposals")
                        .select(
                            "item_id, disposed_qty, status, "
                            "items(item_name, product_code)"
                        )
                        .eq(
                            "user_id",
                            st.session_state.collection_user_id
                        )
                        .eq(
                            "quarter_id",
                            current_quarter["id"]
                        )
                        .execute()
                    )

                    if saved_disposals_result.data:

                        for row in saved_disposals_result.data:

                            item_info = row.get("items")

                            if not item_info:
                                continue

                            col1, col2, col3 = st.columns(
                                [2, 5, 1]
                            )

                            with col1:
                                st.write(
                                    item_info["product_code"]
                                )

                            with col2:
                                st.write(
                                    item_info["item_name"]
                                )

                            with col3:
                                st.write(
                                    f"{row['disposed_qty']}개"
                                )

                    else:

                        st.write(
                            "폐기 요청 내역이 없습니다."
                        )

        # ========================================================
        # 마감 전
        # ========================================================

        else:
            # ----------------------------------------------------
            # 현재 분기의 배분 요청 불러오기
            # ----------------------------------------------------

            # 배분 임시 상태는 폐기 상태와 완전히 분리합니다.
            # 메뉴/모드에서 이탈하면 reset_menu_transition_state()가 이 키를 제거하고,
            # 다시 진입할 때는 DB에 저장된 배분 요청만 다시 불러옵니다.
            distribution_session_key = (
                f"{st.session_state.collection_user_id}_"
                f"_{current_quarter['id']}"
            )

            if (
                st.session_state.get("distribution_loaded_key")
                != distribution_session_key
            ):

                saved_requests = (
                    admin_supabase
                    .table("requests")
                    .select("item_id")
                    .eq(
                        "user_id",
                        st.session_state.collection_user_id
                    )
                    .eq(
                        "quarter_id",
                        current_quarter["id"]
                    )
                    .execute()
                )

                st.session_state.distribution_selected_items = [
                    row["item_id"]
                    for row in saved_requests.data
                ]

                st.session_state.distribution_loaded_key = (
                    distribution_session_key
                )

            if "selected_disposal_items" not in st.session_state:
                st.session_state.selected_disposal_items = []

            # ----------------------------------------------------
            # 배분
            # ----------------------------------------------------
            if collection_mode == "배분":

                with user_content_area:

                    quarter_items_result = (
                        admin_supabase
                        .table("quarter_items")
                        .select(
                            "item_id, distribution_available, "
                            "disposal_available, "
                            "items("
                            "id, item_name, product_code, "
                            "store_name, category_id, image_path, "
                            "is_active, cost_price"
                            ")"
                        )
                        .eq(
                            "quarter_id",
                            current_quarter["id"]
                        )
                        .eq(
                            "distribution_available",
                            True
                        )
                        .execute()
                    )

                    available_items = [
                        row["items"]
                        for row in quarter_items_result.data
                        if (
                            row.get("items")
                            and row["items"].get("is_active")
                        )
                    ]

                    # ------------------------------------------------
                    # 카테고리
                    # ------------------------------------------------

                    category_result = (
                        admin_supabase
                        .table("categories")
                        .select(
                            "id, category_name, parent_id"
                        )
                        .eq(
                            "is_active",
                            True
                        )
                        .order(
                            "category_name"
                        )
                        .execute()
                    )

                    categories = category_result.data

                    major_categories = [
                        category
                        for category in categories
                        if category["parent_id"] is None
                    ]

                    major_category_options = {
                        category["category_name"]:
                        category["id"]
                        for category in major_categories
                    }

                    if major_category_options:

                        category_col, subcategory_col, _ = st.columns(
                            [1, 1, 4],
                            gap="small"
                        )

                        with category_col:

                            st.markdown(
                                """
                                <div style="
                                    font-size: 18px;
                                    font-weight: 700;
                                ">
                                    카테고리 선택
                                </div>
                                <div style="height: 6px;"></div>
                                """,
                                unsafe_allow_html=True
                            )

                            selected_major_name = st.selectbox(
                                "",
                                list(
                                    major_category_options.keys()
                                ),
                                key="user_major_category",
                                label_visibility="collapsed"
                            )

                        selected_major_id = (
                            major_category_options[
                                selected_major_name
                            ]
                        )

                        sub_categories = [
                            category
                            for category in categories
                            if (
                                category["parent_id"]
                                == selected_major_id
                            )
                        ]

                        if sub_categories:

                            sub_category_options = {
                                "전체": None
                            }

                            for category in sub_categories:

                                sub_category_options[
                                    category["category_name"]
                                ] = category["id"]

                            with subcategory_col:

                                st.markdown(
                                    """
                                    <div style="
                                        font-size: 18px;
                                        font-weight: 700;
                                    ">
                                        세부 카테고리
                                    </div>
                                    <div style="height: 6px;"></div>
                                    """,
                                    unsafe_allow_html=True
                                )

                                selected_sub_name = st.selectbox(
                                    "",
                                    list(
                                        sub_category_options.keys()
                                    ),
                                    key="user_sub_category",
                                    label_visibility="collapsed"
                                )

                            selected_sub_id = (
                                sub_category_options[
                                    selected_sub_name
                                ]
                            )

                            if selected_sub_id is None:

                                sub_category_ids = [
                                    category["id"]
                                    for category in sub_categories
                                ]

                                filtered_items = [
                                    item
                                    for item in available_items
                                    if (
                                        item["category_id"]
                                        in sub_category_ids
                                    )
                                ]

                            else:

                                filtered_items = [
                                    item
                                    for item in available_items
                                    if (
                                        item["category_id"]
                                        == selected_sub_id
                                    )
                                ]

                        else:

                            filtered_items = [
                                item
                                for item in available_items
                                if (
                                    item["category_id"]
                                    == selected_major_id
                                )
                            ]

                        # --------------------------------------------
                        # 상품 카드
                        # --------------------------------------------

                        st.write(
                            "상품 수:",
                            len(filtered_items)
                        )

                        cols = st.columns(4)

                        for index, item in enumerate(
                            filtered_items
                        ):

                            with cols[index % 4]:

                                if item["image_path"]:

                                    image_url = (
                                        f"{url}"
                                        f"/storage/v1/object/public/"
                                        f"item-images/"
                                        f"{item['image_path']}"
                                    )

                                    st.image(
                                        image_url,
                                        use_container_width=True
                                    )

                                else:

                                    st.write(
                                        "이미지 없음"
                                    )

                                st.write(
                                    item["item_name"]
                                )

                                code_col, store_col = st.columns(
                                    [1, 1]
                                )

                                with code_col:
                                    st.caption(
                                        item["product_code"]
                                    )

                                with store_col:
                                    st.markdown(
                                        f"<div style='text-align:right; color:#6b7280; font-size:0.8rem;'>{item.get('store_name', '')}</div>",
                                        unsafe_allow_html=True
                                    )

                                if st.button(
                                    "+",
                                    key=(
                                        f"add_collection_"
                                        f"{item['id']}"
                                    )
                                ):

                                    if (
                                        item["id"]
                                        not in
                                        st.session_state.distribution_selected_items
                                    ):

                                        st.session_state.distribution_selected_items.append(
                                            item["id"]
                                        )

                                    safe_rerun()
    # ====================================================
                # 오른쪽 : 배분 요청 목록
                # ====================================================

                with user_request_area:

                    st.subheader(
                        "배분 요청 목록"
                    )

                    if st.session_state.distribution_selected_items:

                        with st.container(
                            border=True,
                            key="request_panel_distribution"
                        ):

                            for selected_item_id in (
                                st.session_state.distribution_selected_items
                            ):

                                selected_item = next(
                                    (
                                        item
                                        for item in available_items
                                        if item["id"] == selected_item_id
                                    ),
                                    None
                                )

                                if not selected_item:
                                    continue

                                col1, col2, col3 = st.columns(
                                    [2, 5, 1]
                                )

                                with col1:
                                    st.write(
                                        selected_item["product_code"]
                                    )

                                with col2:
                                    st.write(
                                        selected_item["item_name"]
                                    )

                                with col3:
                                    if st.button(
                                        "✕",
                                        key=(
                                            f"remove_collection_"
                                            f"{selected_item_id}"
                                        )
                                    ):
                                        st.session_state.distribution_selected_items.remove(
                                            selected_item_id
                                        )
                                        safe_rerun()

                            st.divider()

                            # 선택된 상품 원가 총합계
                            total_cost = 0

                            for selected_item_id in (
                                st.session_state.distribution_selected_items
                            ):

                                selected_item_for_cost = next(
                                    (
                                        item
                                        for item in available_items
                                        if item["id"] == selected_item_id
                                    ),
                                    None
                                )

                                if selected_item_for_cost:

                                    cost_value = (
                                        selected_item_for_cost.get(
                                            "cost_price",
                                            0
                                        )
                                    )

                                    if isinstance(cost_value, str):
                                        cost_value = cost_value.replace(
                                            ",",
                                            ""
                                        ).strip()

                                    try:
                                        total_cost += int(
                                            cost_value or 0
                                        )
                                    except (TypeError, ValueError):
                                        pass

                            # 하단 바: 폐기 요청 목록과 동일한 4열 구조로 저장 버튼 위치 고정
                            bottom_col1, bottom_col2, bottom_col3, bottom_col4 = st.columns(
                                [2, 4, 2, 1],
                                gap="small"
                            )

                            with bottom_col1:

                                st.markdown(
                                    f"""
                                    <div style="
                                        display:flex;
                                        align-items:center;
                                        min-height:40px;
                                        font-size:20px !important;
                                        font-weight:700;
                                        color:#1b4332;
                                        white-space:nowrap;
                                        width:max-content;
                                    " class="save-collection-total-cost">
                                        원가 총합계: {total_cost:,}원
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                            with bottom_col2:
                                st.empty()

                            with bottom_col3:
                                st.empty()

                            with bottom_col4:

                                st.markdown(
                                    """
                                    <style>
                                    [class*="st-key-save_collection_requests"] {
                                        display: flex !important;
                                        justify-content: flex-end !important;
                                        width: 100% !important;
                                    }
                                    [class*="st-key-save_collection_requests"] button {
                                        width: auto !important;
                                        margin-left: auto !important;
                                    }
                                    </style>
                                    """,
                                    unsafe_allow_html=True
                                )

                                save_collection_button = st.button(
                                    "저장",
                                    type="primary",
                                    key="save_collection_requests"
                                )

                            if save_collection_button:

                                try:

                                    (
                                        admin_supabase
                                        .table("requests")
                                        .delete()
                                        .eq(
                                            "user_id",
                                            st.session_state.collection_user_id
                                        )
                                        .eq(
                                            "quarter_id",
                                            current_quarter["id"]
                                        )
                                        .execute()
                                    )

                                    request_rows = [
                                        {
                                            "user_id": st.session_state.collection_user_id,
                                            "item_id": item_id,
                                            "year": current_quarter["year"],
                                            "quarter": current_quarter["quarter"],
                                            "requested_qty": 1,
                                            "status": "requested",
                                            "quarter_id": current_quarter["id"]
                                        }
                                        for item_id in st.session_state.distribution_selected_items
                                    ]

                                    if request_rows:

                                        (
                                            admin_supabase
                                            .table("requests")
                                            .insert(request_rows)
                                            .execute()
                                        )

                                    show_collection_save_message(True)

                                except Exception:

                                    show_collection_save_message(False)

                    else:

                        st.write(
                            "아직 취합한 품목이 없습니다."
                        )


                # ----------------------------------------------------
            # ----------------------------------------------------
            # 폐기
            # ----------------------------------------------------

            else:

                with user_content_area:

                    quarter_items_result = (
                        admin_supabase
                        .table("quarter_items")
                        .select(
                            "item_id, distribution_available, "
                            "disposal_available, "
                            "items("
                            "id, item_name, product_code, "
                            "store_name, category_id, image_path, is_active"
                            ")"
                        )
                        .eq(
                            "quarter_id",
                            current_quarter["id"]
                        )
                        .eq(
                            "disposal_available",
                            True
                        )
                        .execute()
                    )

                    available_items = [
                        row["items"]
                        for row in quarter_items_result.data
                        if (
                            row.get("items")
                            and row["items"].get("is_active")
                        )
                    ]

                    # ------------------------------------------------
                    # 카테고리
                    # ------------------------------------------------

                    category_result = (
                        admin_supabase
                        .table("categories")
                        .select(
                            "id, category_name, parent_id"
                        )
                        .eq(
                            "is_active",
                            True
                        )
                        .order(
                            "category_name"
                        )
                        .execute()
                    )

                    categories = category_result.data

                    major_categories = [
                        category
                        for category in categories
                        if category["parent_id"] is None
                    ]

                    major_category_options = {
                        category["category_name"]:
                        category["id"]
                        for category in major_categories
                    }

                    if major_category_options:

                        category_col, subcategory_col, _ = st.columns(
                            [1, 1, 4],
                            gap="small"
                        )

                        with category_col:

                            st.markdown(
                                """
                                <div style="
                                    font-size: 18px;
                                    font-weight: 700;
                                    margin-bottom: 6px;
                                ">
                                    카테고리 선택
                                </div>
                                """,
                                unsafe_allow_html=True
                            )

                            selected_major_name = st.selectbox(
                                "",
                                list(
                                    major_category_options.keys()
                                ),
                                key="user_major_category",
                                label_visibility="collapsed"
                            )

                        selected_major_id = (
                            major_category_options[
                                selected_major_name
                            ]
                        )

                        sub_categories = [
                            category
                            for category in categories
                            if (
                                category["parent_id"]
                                == selected_major_id
                            )
                        ]

                        if sub_categories:

                            sub_category_options = {
                                "전체": None
                            }

                            for category in sub_categories:

                                sub_category_options[
                                    category["category_name"]
                                ] = category["id"]

                            with subcategory_col:

                                st.markdown(
                                    """
                                    <div style="
                                        font-size: 18px;
                                        font-weight: 700;
                                        margin-bottom: 6px;
                                    ">
                                        세부 카테고리
                                    </div>
                                    """,
                                    unsafe_allow_html=True
                                )

                                selected_sub_name = st.selectbox(
                                    "",
                                    list(
                                        sub_category_options.keys()
                                    ),
                                    key="user_sub_category",
                                    label_visibility="collapsed"
                                )

                            selected_sub_id = (
                                sub_category_options[
                                    selected_sub_name
                                ]
                            )

                            if selected_sub_id is None:

                                sub_category_ids = [
                                    category["id"]
                                    for category in sub_categories
                                ]

                                filtered_items = [
                                    item
                                    for item in available_items
                                    if (
                                        item["category_id"]
                                        in sub_category_ids
                                    )
                                ]

                            else:

                                filtered_items = [
                                    item
                                    for item in available_items
                                    if (
                                        item["category_id"]
                                        == selected_sub_id
                                    )
                                ]

                        else:

                            filtered_items = [
                                item
                                for item in available_items
                                if (
                                    item["category_id"]
                                    == selected_major_id
                                )
                            ]

                        # --------------------------------------------
                        # 상품 카드
                        # --------------------------------------------

                        st.write(
                            "상품 수:",
                            len(filtered_items)
                        )

                        cols = st.columns(4)

                        for index, item in enumerate(
                            filtered_items
                        ):

                            with cols[index % 4]:

                                if item["image_path"]:

                                    image_url = (
                                        f"{url}"
                                        f"/storage/v1/object/public/"
                                        f"item-images/"
                                        f"{item['image_path']}"
                                    )

                                    st.image(
                                        image_url,
                                        use_container_width=True
                                    )

                                else:

                                    st.write(
                                        "이미지 없음"
                                    )

                                st.write(
                                    item["item_name"]
                                )

                                code_col, store_col = st.columns(
                                    [1, 1]
                                )

                                with code_col:
                                    st.caption(
                                        item["product_code"]
                                    )

                                with store_col:
                                    st.markdown(
                                        f"<div style='text-align:right; color:#6b7280; font-size:0.8rem;'>{item.get('store_name', '')}</div>",
                                        unsafe_allow_html=True
                                    )

                                if st.button(
                                    "+",
                                    key=(
                                        f"add_disposal_"
                                        f"{item['id']}"
                                    )
                                ):

                                    if (
                                        item["id"]
                                        not in
                                        st.session_state.selected_disposal_items
                                    ):

                                        st.session_state.selected_disposal_items.append(
                                            item["id"]
                                        )

                                    safe_rerun()

                with user_request_area:

                    disposal_session_key = (
                        f"{st.session_state.collection_user_id}_"
                        f"{current_quarter['id']}"
                    )

                    if (
                        st.session_state.get(
                            "disposal_loaded_key"
                        )
                        != disposal_session_key
                    ):

                        existing_disposal_result = (
                            admin_supabase
                            .table("disposals")
                            .select(
                                "item_id, disposed_qty"
                            )
                            .eq(
                                "user_id",
                                st.session_state.collection_user_id
                            )
                            .eq(
                                "quarter_id",
                                current_quarter["id"]
                            )
                            .execute()
                        )

                        st.session_state.selected_disposal_items = [
                            row["item_id"]
                            for row in existing_disposal_result.data
                        ]

                        for row in existing_disposal_result.data:

                            st.session_state[
                                f"disposal_qty_{row['item_id']}"
                            ] = row["disposed_qty"]

                        st.session_state.disposal_loaded_key = (
                            disposal_session_key
                        )

                    st.subheader("폐기 요청 목록")

                    valid_selected_disposal_items = [
                        item_id
                        for item_id in st.session_state.selected_disposal_items
                        if any(
                            item["id"] == item_id
                            for item in available_items
                        )
                    ]

                    st.session_state.selected_disposal_items = (
                        valid_selected_disposal_items
                    )

                    if valid_selected_disposal_items:

                        with st.container(
                            border=True,
                            key="request_panel_disposal"
                        ):

                            inventory_result = (
                                admin_supabase
                                .table("user_inventory")
                                .select("item_id, current_qty")
                                .eq(
                                    "user_id",
                                    st.session_state.collection_user_id
                                )
                                .execute()
                            )

                            inventory_map = {
                                row["item_id"]: row["current_qty"]
                                for row in inventory_result.data
                            }

                            for selected_item_id in valid_selected_disposal_items:

                                selected_item = next(
                                    (
                                        item
                                        for item in available_items
                                        if item["id"] == selected_item_id
                                    ),
                                    None
                                )

                                if not selected_item:
                                    continue

                                current_qty = inventory_map.get(
                                    selected_item_id,
                                    0
                                )

                                col1, col2, col3, col4 = st.columns(
                                    [2, 4, 2, 1]
                                )

                                with col1:
                                    st.write(
                                        selected_item["product_code"]
                                    )

                                with col2:
                                    st.write(
                                        selected_item["item_name"]
                                    )

                                with col3:
                                    st.number_input(
                                        f"폐기 수량 (보유 {current_qty}개)",
                                        min_value=0,
                                        max_value=current_qty,
                                        step=1,
                                        value=0,
                                        key=(
                                            f"disposal_qty_"
                                            f"{selected_item_id}"
                                        ),
                                        label_visibility="collapsed"
                                    )

                                with col4:
                                    if st.button(
                                        "✕",
                                        key=(
                                            f"remove_disposal_"
                                            f"{selected_item_id}"
                                        )
                                    ):
                                        st.session_state.selected_disposal_items.remove(
                                            selected_item_id
                                        )
                                        safe_rerun()

                            st.divider()

                            # X 버튼이 있는 마지막 열과 동일한 우측 끝선에 저장 버튼 배치
                            disposal_save_col1, disposal_save_col2, disposal_save_col3, disposal_save_col4 = st.columns(
                                [2, 4, 2, 1],
                                gap="small"
                            )

                            with disposal_save_col1:
                                st.empty()

                            with disposal_save_col2:
                                st.empty()

                            with disposal_save_col3:
                                st.empty()

                            with disposal_save_col4:
                                st.markdown(
                                    """
                                    <style>
                                    [class*="st-key-save_disposals"] {
                                        display: flex !important;
                                        justify-content: flex-end !important;
                                        width: 100% !important;
                                    }
                                    [class*="st-key-save_disposals"] button {
                                        width: auto !important;
                                        margin-left: auto !important;
                                    }
                                    </style>
                                    """,
                                    unsafe_allow_html=True
                                )

                                disposal_save_button = st.button(
                                    "저장",
                                    type="primary",
                                    key="save_disposals"
                                )

                            if disposal_save_button:

                                disposal_rows = []

                                for selected_item_id in (
                                    st.session_state.selected_disposal_items
                                ):

                                    disposal_qty = st.session_state.get(
                                        f"disposal_qty_{selected_item_id}",
                                        0
                                    )

                                    if disposal_qty > 0:

                                        disposal_rows.append(
                                            {
                                                "user_id": st.session_state.collection_user_id,
                                                "item_id": selected_item_id,
                                                "disposed_qty": disposal_qty,
                                                "status": "pending",
                                                "quarter_id": current_quarter["id"]
                                            }
                                        )

                                if not disposal_rows:

                                    show_disposal_quantity_warning()

                                else:

                                    for disposal_row in disposal_rows:

                                        existing_result = (
                                            admin_supabase
                                            .table("disposals")
                                            .select("id, status")
                                            .eq(
                                                "quarter_id",
                                                disposal_row["quarter_id"]
                                            )
                                            .eq(
                                                "user_id",
                                                disposal_row["user_id"]
                                            )
                                            .eq(
                                                "item_id",
                                                disposal_row["item_id"]
                                            )
                                            .limit(1)
                                            .execute()
                                        )

                                        if existing_result.data:

                                            existing_disposal = existing_result.data[0]

                                            if existing_disposal["status"] == "approved":

                                                show_disposal_approved_warning()

                                            else:

                                                (
                                                    admin_supabase
                                                    .table("disposals")
                                                    .update(
                                                        {
                                                            "disposed_qty": disposal_row["disposed_qty"],
                                                            "status": "pending"
                                                        }
                                                    )
                                                    .eq(
                                                        "id",
                                                        existing_disposal["id"]
                                                    )
                                                    .execute()
                                                )

                                        else:

                                            (
                                                admin_supabase
                                                .table("disposals")
                                                .insert(disposal_row)
                                                .execute()
                                            )

                                    show_disposal_save_complete()

                    else:

                        st.write(
                            "아직 취합한 품목이 없습니다."
                        )




# -----------------------------------------------------------------------------
# 전체 화면/모달의 위험·삭제·취소·제거 버튼 색상 통일
# 기존 기능/로직에는 영향을 주지 않고 버튼 스타일만 덮어쓴다.
# -----------------------------------------------------------------------------
st.markdown(
    """
    <style>
    [class*="st-key-modal_delete_order_items"] button,
    [class*="st-key-modal_cancel_add_user"] button,
    [class*="st-key-modal_confirm_delete_"] button,
    [class*="st-key-modal_cancel_delete_"] button,
    [class*="st-key-modal_delete_user_"] button,
    [class*="st-key-modal_cancel_edit_user_"] button,
    [class*="st-key-bulk_delete_row_"] button,
    [class*="st-key-bulk_item_cancel_"] button,
    [class*="st-key-modal_cancel_quarter"] button,
    [class*="st-key-modal_delete_quarter_"] button,
    [class*="st-key-delete_inventory_modal_"] button,
    [class*="st-key-cancel_inventory_modal_"] button,
    [class*="st-key-confirm_edit_item_delete_"] button,
    [class*="st-key-cancel_edit_item_delete_"] button,
    [class*="st-key-delete_from_edit_item_"] button,
    [class*="st-key-confirm_disposals"] button,
    [class*="st-key-cancel_disposal_confirmation"] button,
    [class*="st-key-delete_disposals"] button,
    [class*="st-key-remove_collection_"] button,
    [class*="st-key-remove_disposal_"] button {
        background: #2e8b57 !important;
        background-color: #2e8b57 !important;
        border-color: #2e8b57 !important;
        color: #ffffff !important;
        box-shadow: none !important;
    }

    [class*="st-key-modal_delete_order_items"] button:hover,
    [class*="st-key-modal_cancel_add_user"] button:hover,
    [class*="st-key-modal_confirm_delete_"] button:hover,
    [class*="st-key-modal_cancel_delete_"] button:hover,
    [class*="st-key-modal_delete_user_"] button:hover,
    [class*="st-key-modal_cancel_edit_user_"] button:hover,
    [class*="st-key-bulk_delete_row_"] button:hover,
    [class*="st-key-bulk_item_cancel_"] button:hover,
    [class*="st-key-modal_cancel_quarter"] button:hover,
    [class*="st-key-modal_delete_quarter_"] button:hover,
    [class*="st-key-delete_inventory_modal_"] button:hover,
    [class*="st-key-cancel_inventory_modal_"] button:hover,
    [class*="st-key-confirm_edit_item_delete_"] button:hover,
    [class*="st-key-cancel_edit_item_delete_"] button:hover,
    [class*="st-key-delete_from_edit_item_"] button:hover,
    [class*="st-key-confirm_disposals"] button:hover,
    [class*="st-key-cancel_disposal_confirmation"] button:hover,
    [class*="st-key-delete_disposals"] button:hover,
    [class*="st-key-remove_collection_"] button:hover,
    [class*="st-key-remove_disposal_"] button:hover {
        background: #26734a !important;
        background-color: #26734a !important;
        border-color: #26734a !important;
        color: #ffffff !important;
    }

    [class*="st-key-remove_collection_"] button p,
    [class*="st-key-remove_disposal_"] button p,
    [class*="st-key-modal_delete_order_items"] button p,
    [class*="st-key-modal_confirm_delete_"] button p,
    [class*="st-key-modal_delete_user_"] button p,
    [class*="st-key-modal_delete_quarter_"] button p,
    [class*="st-key-delete_inventory_modal_"] button p,
    [class*="st-key-confirm_edit_item_delete_"] button p,
    [class*="st-key-delete_from_edit_item_"] button p,
    [class*="st-key-confirm_disposals"] button p,
    [class*="st-key-cancel_disposal_confirmation"] button p,
    [class*="st-key-delete_disposals"] button p {
        color: #ffffff !important;
    }

    div[data-testid="stColumn"]:has(button[key^="admin_menu_"]) button:hover,
    div[data-testid="stColumn"]:has(button[key="user_mode_distribution"]) button:hover,
    div[data-testid="stColumn"]:has(button[key="user_mode_disposal"]) button:hover,
    div[data-testid="stColumn"]:has(button[key="user_menu_inventory"]) button:hover {
        color: #2e8b57 !important;
    }
    </style>
    """,
    unsafe_allow_html=True
)
