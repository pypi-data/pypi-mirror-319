import streamlit as st
from typing import Any, Union, TypeAlias
from pathlib import PosixPath
Key: TypeAlias = Union[str, int]

class PageSessionState:
    def __init__(self, file_path: str|PosixPath):
        self._file_path = str(file_path)

    def set_if_not_exist(self, name_vals: dict):
        for name, val in name_vals.items():
            sname = self._name2session_name(name)
            if sname not in st.session_state:
                st.session_state[sname] = val
    def _name2session_name(self, name):
        return f"{self._file_path}_{name}"

    def _set_session_value(self, name, value):
        sname = self._name2session_name(name)
        st.session_state[sname] = value

    def _get_sesseion_value(self, name):
        sname = self._name2session_name(name)
        return st.session_state[sname]

    def _get_all_keys(self, is_remove_file_path: bool = True) -> list[str]:
        dst_keys = [key for key in st.session_state if key.startswith(self._file_path)]
        if is_remove_file_path:
            dst_keys = [key.replace(f"{self._file_path}_", "") for key in dst_keys]
        return dst_keys
    
    def __call__(self, key: Key) -> Key:
        return self._name2session_name(name=key)

    def __setitem__(self, key: Key, value: Any) -> None:
        key = str(key)
        self._set_session_value(key, value)
    
    def __getitem__(self, key: Key) -> Any:
        key = str(key)
        return self._get_sesseion_value(key)

    def __contains__(self, key: Key) -> bool:
        return key in self._get_all_keys()

    def __setattr__(self, name, value):
        # 実際に属性に値を設定する
        if name == "_file_path":
            super().__setattr__(name, value)
        else:
            self._set_session_value(name, value)

    def __getattribute__(self, name):
        if name in [
            "_file_path",
            "_name2session_name",
            "_set_session_value",
            "_get_sesseion_value",
            "set_if_not_exist",
            "_get_all_keys"]:
            return super().__getattribute__(name)
        return self._get_sesseion_value(name)