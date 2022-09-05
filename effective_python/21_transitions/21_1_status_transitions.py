import asyncio

from transitions import Machine


class Device(object):
    states = ['0', '1', '2', '3', '4', '5', '6', '7', '8', '9']
    # 状态计算优先级，从低到高
    compute_seq = ['normal_standby', 'working', 'exception_standby', 'starving', 'full', 'exception', 'off_line',
                   'emergency_stop', 'debug', 'off']
    states_mapper = {
        'off': '0',
        'working': '1',
        'normal_standby': '2',
        'exception': '3',
        'exception_standby': '4',
        'starving': '5',
        'full': '6',
        'emergency_stop': '8',
        'debug': '9'
    }

    def __init__(self, last_status):
        self.last_status = last_status
        self.machine = Machine(model=self, states=Device.states, initial=str(self.last_status))

    def init_compute_config_of_device(self) -> None:
        # 将数据库中存储的设备相关云管控配置重新解析，并将对应的设备状态计算函数初始化
        # 在完成计算函数初始化之后，获取设备相关点位最新状态数据
        device_compute_config = {
            "working": {
                "status_str": "开机",
                "status_compute_type": "any",
                "status_target_value": 1,
                "related_codes": [
                    "device_a5zdjzdy_1p_1"
                ]
            },
            "exception": {
                "status_str": "故障",
                "status_compute_type": "any",
                "status_target_value": 1,
                "related_codes": [
                    "device_a5zdjzdy_1p_2",
                    "device_a5zdjzdy_1p_8",
                    "device_a5zdjzdy_1p_17",
                    "device_a5zdjzdy_1p_18",
                    "device_a5zdjzdy_1p_19"
                ]
            },
            "normal_standby": {
                "status_str": "正常待机",
                "status_compute_type": "any",
                "status_target_value": "1",
                "related_codes": [
                    "device_a5zdjzdy_1p_3",
                    "device_a5zdjzdy_1p_4",
                    "device_a5zdjzdy_1p_5",
                    "device_a5zdjzdy_1p_6",
                    "device_a5zdjzdy_1p_7",
                    "device_a5zdjzdy_1p_9",
                    "device_a5zdjzdy_1~p_kgj_plc"
                ]
            },
            "off": {
                "status_str": "关机",
                "status_compute_type": "value",
                "status_target_value": "0",
                "related_codes": [
                    "device_a5zdjzdy_1~p_kgj_plc"
                ]
            },
            "debug": {
                "status_str": "调试",
                "status_compute_type": "value",
                "status_target_value": "1",
                "related_codes": [
                    "device_a5zdjzdy_1~device_debug"
                ]
            }
        }
        if device_compute_config:
            for device_status, config in device_compute_config.items():
                setattr(self, f'{device_status}_compute_config', config)

    def init_transition_of_device(self) -> None:
        self.init_compute_config_of_device()
        for device_status, target_status in self.states_mapper.items():
            if hasattr(self, f'{device_status}_compute_config'):
                self.machine.add_transition(device_status, '*', target_status, conditions=[f'is_{device_status}'],
                                            after='new_status_computed')


if __name__ == '__main__':
    obj = Device("3")
    obj.init_transition_of_device()
    print(obj.state)