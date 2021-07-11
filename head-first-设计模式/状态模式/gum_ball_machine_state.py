from random import randint


def winner_random():
    random_num = randint(0, 3)
    return random_num == 1


class SoldStateError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class SoldOutStateError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class NoQuarterStateError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class HasQuarterStateError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class WinnerStateError(Exception):
    def __init__(self, *args, **kwargs):
        pass


class State:
    def insert_quarter(self):
        raise NotImplemented

    def eject_quarter(self):
        raise NotImplemented

    def turn_crank(self):
        raise NotImplemented

    def dispense(self):
        raise NotImplemented


class GumBallMachine:
    """
        对外暴露的操作, 只有4个
        1. 插入硬币: insert_quarter()
        2. 退还硬币: eject_quarter()
        3. 转动曲柄: turn_crank()
        4. 恢复初始状态: refill()
    """

    def __init__(self, gumball_number: int):
        self.sold_out_state = SoldOutState(self)
        self.no_quarter_state = NoQuarterState(self)
        self.has_quarter_state = HasQuarterState(self)
        self.sold_state = SoldState(self)
        self.winner_state = WinnerState(self)

        self.refill(gumball_number)

    def insert_quarter(self):
        """ 插入硬币 """
        self.state.insert_quarter()
        print('插入硬币, 当前机器剩余糖果为{}个!'.format(self.get_account()))

    def eject_quarter(self):
        """ 退还硬币 """
        self.state.eject_quarter()
        print('退还硬币, 当前机器剩余糖果为{}个!'.format(self.get_account()))

    def turn_crank(self):
        """ 转动曲柄 """
        try:
            self.state.turn_crank()
        except Exception as error:
            raise error
        else:
            self.state.dispense()
        print('转动曲柄, 当前机器剩余糖果为{}个!'.format(self.get_account()))

    def refill(self, gumball_number=0):
        """ 初始化设备状态 """
        assert gumball_number >= 0, '糖果机中, 糖果的初始数量不能为空!'
        if gumball_number == 0:
            # 处于售空状态
            self.state = self.sold_out_state
        else:
            # 初始化, 处于没有插入硬币状态
            self.state = self.no_quarter_state
        self.count = gumball_number

    def set_state(self, state: State):
        if not isinstance(state, State):
            raise TypeError('state must subclass of State!')
        print('设备状态扭转, old state: {} to new state: {}!'
              ''.format(type(self.state).__name__, type(state).__name__))
        self.state = state

    def get_account(self):
        return self.count

    def release_ball(self):
        if self.count == 0:
            raise AttributeError("当前糖果数量为0, 无法进行出售操作!")
        elif self.count < 0:
            raise AttributeError("当前糖果数量为: {}, 无法进行出售操作!".format(self.count))
        else:
            self.count -= 1

    def get_has_quarter_state(self) -> State:
        return self.has_quarter_state

    def get_no_quarter_state(self) -> State:
        return self.no_quarter_state

    def get_sold_out_state(self) -> State:
        return self.sold_out_state

    def get_sold_state(self) -> State:
        return self.sold_state

    def get_winner_state(self) -> State:
        return self.winner_state


class SoldState(State):
    def __init__(self, gumBallMachine: GumBallMachine):  # 糖果机的引用对象
        self.gumballMachine = gumBallMachine

    def insert_quarter(self):
        raise SoldStateError("出售糖果中, 无法进行投币操作!")

    def eject_quarter(self):
        raise SoldStateError("出售糖果中, 无法进行退款操作!")

    def turn_crank(self):
        raise SoldStateError("出售糖果中, 不要重复拉动曲柄!")

    def dispense(self):
        self.gumballMachine.release_ball()
        if self.gumballMachine.get_account() > 0:
            # 转换到没有硬币状态
            self.gumballMachine.set_state(self.gumballMachine.get_no_quarter_state())
        else:
            # 转到告罄状态
            self.gumballMachine.set_state(self.gumballMachine.get_sold_out_state())


class WinnerState(State):
    def __init__(self, gumBallMachine: GumBallMachine):
        self.gumballMachine = gumBallMachine

    def insert_quarter(self):
        raise WinnerStateError("胜利者状态: 发放糖果中,请不要投币!")

    def eject_quarter(self):
        raise WinnerStateError("胜利者状态: 发糖果中,无法进行退款操作!")

    def turn_crank(self):
        raise WinnerStateError("胜利者状态: 正在发送糖果,重复拉动是无效的哦!")

    def dispense(self):
        self.gumballMachine.release_ball()
        if self.gumballMachine.get_account() > 0:
            self.gumballMachine.release_ball()
            if self.gumballMachine.get_account() == 0:
                self.gumballMachine.set_state(self.gumballMachine.get_sold_out_state())
            self.gumballMachine.set_state(self.gumballMachine.get_no_quarter_state())
        elif self.gumballMachine.get_account() == 0:
            self.gumballMachine.set_state(self.gumballMachine.get_sold_out_state())
        else:
            raise WinnerStateError("胜利者状态: 分发糖果异常, 糖果分发为负!")


class SoldOutState(State):
    def __init__(self, gumBallMachine: GumBallMachine):  # 糖果机的引用对象
        self.gumballMachine = gumBallMachine

    def insert_quarter(self):
        raise SoldOutStateError("告罄状态: 没有糖果了,请不要投币!")

    def eject_quarter(self):
        raise SoldOutStateError("告罄状态: 没有糖果了,无法进行退还操作!")

    def turn_crank(self):
        raise SoldOutStateError("告罄状态: 没有糖果,转动无效!")

    def dispense(self):
        raise SoldOutStateError("告罄状态: 无法进行糖果的分发!")


class NoQuarterState(State):
    def __init__(self, gumBallMachine: GumBallMachine):  # 糖果机的引用对象
        self.gumballMachine = gumBallMachine

    def insert_quarter(self):
        self.gumballMachine.set_state(self.gumballMachine.get_has_quarter_state())

    def eject_quarter(self):
        raise NoQuarterStateError("没投币: 不能进行退款操作!")

    def turn_crank(self):
        raise NoQuarterStateError("没投币: 拉动曲柄无效!")

    def dispense(self):
        raise NoQuarterStateError("没投币: 无法进行糖果的分发!")


class HasQuarterState(State):
    def __init__(self, gumBallMachine: GumBallMachine):  # 糖果机的引用对象
        self.gumballMachine = gumBallMachine

    def insert_quarter(self):
        raise HasQuarterStateError("投币状态: 请不要重复投币!")

    def eject_quarter(self):
        self.gumballMachine.set_state(self.gumballMachine.get_no_quarter_state())

    def turn_crank(self):
        if winner_random() and self.gumballMachine.get_account() > 1:
            self.gumballMachine.set_state(self.gumballMachine.get_winner_state())
        else:
            self.gumballMachine.set_state(self.gumballMachine.get_sold_state())

    def dispense(self):
        raise HasQuarterStateError("投币状态: 等待拉动曲柄!")


if __name__ == '__main__':
    from datetime import datetime, timedelta

    current_time = datetime.now()
    test_date = datetime.strptime('2021-07-09 06:50:00', '%Y-%m-%d %H:%M:%S')
    # "shift": "早班" if (6, 50) <= (x["start_time"].hour, x["start_time"].minute) < (18, 50) else "晚班",
    print(datetime.strftime(current_time, "%Y-%m-%d %H:%M:%S"))
    print(100 > timedelta(seconds=34))
    current_banci = "早班" if (6, 50) <= (test_date.hour, test_date.minute) < (18, 50) else "晚班"
    # "早班" if (6, 50) <= (x["start_time"].hour,x["start_time"].minute) < (18, 50) else "晚班"
    print(current_banci)
    print((current_time.hour, current_time.minute))
    # print(current_banci)
    # gumballModel = GumBallMachine(5)
    # gumballModel.insert_quarter()
    # gumballModel.turn_crank()
    #
    # gumballModel.insert_quarter()
    #
    # gumballModel.turn_crank()
    # gumballModel.eject_quarter()
    #
    # gumballModel.insert_quarter()
    # gumballModel.turn_crank()
    #
    # gumballModel.insert_quarter()
    # gumballModel.turn_crank()
    #
    # gumballModel.insert_quarter()
    # gumballModel.turn_crank()
    #
    # gumballModel.insert_quarter()
    # gumballModel.turn_crank()
