# coding: utf8
""" 
@File: _database.py
@Editor: PyCharm
@Author: Austin (From Chengdu.China) https://fairy.host
@HomePage: https://github.com/AustinFairyland
@OperatingSystem: Windows 11 Professional Workstation 23H2 Canary Channel
@CreatedTime: 2023-10-12
"""
from __future__ import annotations

import abc
import os
import sys
import warnings
import platform
import asyncio

sys.dont_write_bytecode = True
warnings.filterwarnings("ignore")
if platform.system() == "Windows":
    asyncio.set_event_loop_policy(asyncio.WindowsSelectorEventLoopPolicy())

import typing
import types
from typing import Union, Any, Callable, overload, List, Tuple, Dict
from abc import ABC, abstractmethod
import pymysql
from pymysql.connections import Connection
from pymysql.cursors import Cursor

from fairyland.framework.modules.journal import Journal
from fairyland.framework.utils.abnormal import SQLExecutionError


class BaseDataSourceUtils(ABC):
    def __init__(
        self,
        host: str = "127.0.0.1",
        port: int = 3306,
        user: str = "root",
        password: str = "",
        database: str = "",
        charset: str = "utf8mb4",
        connect_timeout: int = 10,
    ):
        """
        Initialize datasource info.
            初始化数据源信息。
        @param host: Database host address. | 数据库主机地址
        @type host: str
        @param port: Database port. | 数据库端口
        @type port: int
        @param user: Database username. | 数据库用户名
        @type user: str
        @param password: Database password. | 数据库密码
        @type password: str
        @param database: Database name to connect to. | 要连接的数据库名称
        @type database: str
        """
        self.host = host
        self.port = port
        self.user = user
        self.password = password
        self.database = database
        self.charset = charset
        self.connect_timeout = connect_timeout
        self.connection = self.connect()
        self.cursor = self.__create_cursor()

    @abstractmethod
    def connect(self) -> Connection:
        """
        Initialize datasource connection.
            初始化连接
        @return: Database Connect Object. | 数据库连接对象
        @rtype: DataBase Object. | 数据库连接对象
        """
        try:
            connect = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                connect_timeout=self.connect_timeout,
            )
            Journal.success("MySQL Connect: OK")
        except Exception as error:
            Journal.error(error)
            raise
        return connect

    def __create_cursor(self) -> Cursor:
        """
        Create the database cursor.
            创建数据库游标
        @return: DataBase Cursor Object. | 数据库游标对象
        @rtype: DataBase Cursor Object. | 数据库游标对象
        """
        return self.connection.cursor()

    def __close_cursor(self) -> None:
        """
        Close the database cursor.
            关闭数据库游标。
        """
        if self.cursor:
            self.cursor.close()
            self.cursor = None
            Journal.warning("Database has disconnected the cursor.")

    def __close_connect(self) -> None:
        """
        Close the database connection.
            关闭数据库连接。
        """
        if self.connection:
            self.connection.close()
            self.connection = None
            Journal.warning("Database has been disconnected.")

    def __reconnect(self) -> None:
        """
        Reconnect to the database.
            重连数据库。
        """
        if self.connection and not self.cursor:
            Journal.warning("Database is connected.")
            self.cursor = self.__create_cursor()
            Journal.warning("Database cursor has been reconnected.")
        else:
            self.connection = self.connect()
            Journal.warning("Database has been reconnected.")
            self.cursor = self.__create_cursor()
            Journal.warning("Database cursor has been reconnected.")

    def __close(self) -> None:
        """
        Completely close the database connection and cursor.
            完全关闭数据库连接和游标。
        """
        if self.cursor:
            self.__close_cursor()
        if self.connection:
            self.__close_connect()
        Journal.warning("Database has been disconnected the all.")

    def __trace_sql_statement(self, statement, parameters) -> str:
        """
        Generate and return a debug SQL statements.
            生成并返回调试SQL语句。
        @param statement: SQL statements statements. | SQL查询语句
        @type statement: str
        @param parameters: SQL statements parameters. | SQL查询参数
        @type parameters: Union[tuple, list, dict, None]
        @return: Debug information. | 调试信息
        @rtype: str
        """
        return f"SQL Statement -> {statement} | Parameters -> {parameters}"

    @abstractmethod
    def execute(self, statement: str, parameters: Union[str, tuple, list, None] = None) -> None:
        self.cursor.execute(query=statement, args=parameters)

    def __operation(
        self,
        statements: Union[str, tuple, list, set],
        parameters: Union[tuple, list, dict, None] = None,
    ) -> Tuple:
        """
        Execute SQL operations.
            执行 SQL 操作。
        @param statements: SQL statement(s). SQL语句
        @type statements: Union[str, tuple, list, set]
        @param parameters: SQL parameters. | SQL参数
        @type parameters: Union[tuple, list, dict, None]
        @return: Operation result. | 操作结果
        @rtype: Depends on the SQL operation
        """
        try:
            self.__reconnect()
            if isinstance(statements, str):
                Journal.trace(self.__trace_sql_statement(statements, parameters))
                self.execute(statement=statements, parameters=parameters)
                results = self.cursor.fetchall()
            elif isinstance(statements, (tuple, list, set)):
                results_list = []
                for query_str, query_parameters in zip(statements, parameters):
                    Journal.trace(self.__trace_sql_statement(query_str, query_parameters))
                    self.execute(statement=statements, parameters=parameters)
                    results_list.append(self.cursor.fetchall())
            else:
                raise TypeError("Wrong SQL statements type.")
            self.connection.commit()
        except Exception as error:
            Journal.debug("Failed to execute the rollback")
            self.connection.rollback()
            Journal.error(error)
            raise
        finally:
            self.__close_cursor()
        return results if "results" in locals() else tuple(results_list)

    def operation(
        self,
        statements: Union[str, tuple, list, set],
        parameters: Union[tuple, list, dict, None] = None,
    ) -> Tuple:
        """
        Execute single or multiple SQL statements.
            执行单个或多个 SQL 语句。
        @param statements: SQL statements or a set of statements. | SQL语句或语句集
        @type statements: Union[str, tuple, list, set]
        @param parameters: Parameters for the SQL statements(s). | SQL语句的参数
        @type parameters: Union[tuple, list, dict, None]
        @return: Execution result. | 执行结果
        @rtype: Depends on the SQL operation
        """
        if not isinstance(statements, str) and isinstance(statements, (list, tuple, set)) and not parameters:
            parameters = tuple([None for _ in range(len(statements))])
        return self.__operation(statements=statements, parameters=parameters)

    def close(self) -> None:
        """
        Close the database connection and cursor.
            关闭数据库连接和游标。
        """
        self.__close()


class MySQLUtils(BaseDataSourceUtils):

    def __init__(self, *args: Any, **kwargs: Any):
        super().__init__(*args, **kwargs)

    def connect(self) -> Connection:
        try:
            connect = pymysql.connect(
                host=self.host,
                port=self.port,
                user=self.user,
                password=self.password,
                database=self.database,
                charset=self.charset,
                connect_timeout=self.connect_timeout,
            )
            Journal.success("MySQL Connect: OK")
        except Exception as error:
            Journal.error(error)
            raise
        return connect

    def execute(self, statement: str, parameters: Union[str, tuple, list, None] = None) -> None:
        self.cursor.execute(query=statement, args=parameters)
