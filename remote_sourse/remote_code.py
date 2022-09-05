from fabric2 import Connection

if __name__ == '__main__':
    fabric2_conn = Connection('124.223.182.33', user="root", port=22, connect_kwargs={'password': "Leichao2022"})
    execute_cmd_str = "ps -ef | grep python | grep -v grep"
    run_cmd_rcd = fabric2_conn.run(execute_cmd_str)
    fabric2_conn.run("top")
