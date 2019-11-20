import random
import math
import game_framework
from BehaviorTree import BehaviorTree, SelectorNode, SequenceNode, LeafNode
from pico2d import *
import main_state

# zombie Run Speed
PIXEL_PER_METER = (10.0 / 0.3)  # 10 pixel 30 cm
RUN_SPEED_KMPH = 20.0  # Km / Hour
RUN_SPEED_MPM = (RUN_SPEED_KMPH * 1000.0 / 60.0)
RUN_SPEED_MPS = (RUN_SPEED_MPM / 60.0)
RUN_SPEED_PPS = (RUN_SPEED_MPS * PIXEL_PER_METER)

# zombie Action Speed
TIME_PER_ACTION = 0.5
ACTION_PER_TIME = 1.0 / TIME_PER_ACTION
FRAMES_PER_ACTION = 10

animation_names = ['Attack', 'Dead', 'Idle', 'Walk']


class Zombie:
    images = None

    def load_images(self):
        if Zombie.images == None:
            Zombie.images = {}
            for name in animation_names:
                Zombie.images[name] = [load_image("./zombiefiles/female/" + name + " (%d)" % i + ".png") for i in
                                       range(1, 11)]

    def __init__(self):
        positions = [(43, 750), (1118, 750), (1050, 530), (575, 220), (235, 33), (575, 220), (1050, 530), (1118, 750)]
        self.patrol_positions = []
        for p in positions:
            self.patrol_positions.append((p[0], 1024 - p[1]))  # convert for origin at bottom,left
        self.patrol_order = 1
        self.target_x, self.target_y = None, None
        self.x, self.y = self.patrol_positions[0]

        self.load_images()
        self.dir = random.random() * 2 * math.pi  # random moving direction
        self.speed = 0
        self.timer = 1.0  # change direction every 1 sec when wandering
        self.frame = 0
        self.build_behavior_tree()
        self.font = load_font('ENCR10B.TTF', 16)
        self.hp = 0

    def calculate_current_position(self):
        self.frame = (self.frame + FRAMES_PER_ACTION * ACTION_PER_TIME * game_framework.frame_time) % FRAMES_PER_ACTION
        self.x += self.speed * math.cos(self.dir) * game_framework.frame_time
        self.y += self.speed * math.sin(self.dir) * game_framework.frame_time
        self.x = clamp(50, self.x, 1280 - 50)
        self.y = clamp(50, self.y, 1024 - 50)

    def die(self):
        self.x, self.y = self.patrol_positions[random.randint(0, 5)]
        self.hp = 0

    def wander(self):
        # fill here
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        self.timer -= game_framework.frame_time
        if self.timer < 0:
            self.timer += 1.0
            self.dir = random.random() * 2 * math.pi

        return BehaviorTree.SUCCESS
        pass

    def find_player(self):
        # fill here
        boy = main_state.get_boy()
        distance = (boy.x - self.x) ** 2 + (boy.y - self.y) ** 2
        if distance < (PIXEL_PER_METER * 8) ** 2:
            if self.hp > boy.hp:
                self.dir = math.atan2(boy.y - self.y, boy.x - self.x)
            elif self.hp <= boy.hp:
                self.dir = math.atan2(self.y - boy.y, self.x - boy.x)
            return BehaviorTree.SUCCESS
        else:
            self.speed = 0
            return BehaviorTree.FAIL
        pass

    def find_ball(self):
        balls = main_state.get_ball()
        distance = 0
        nearest_x, nearest_y = 0, 0
        for ball in balls:
            temp = (ball.x - self.x) ** 2 + (ball.y - self.y) ** 2
            if distance <= temp:
                distance = temp
                nearest_x, nearest_y = ball.x, ball.y
        if distance < (PIXEL_PER_METER * 5) ** 2:
            self.dir = math.atan2(nearest_y - self.y, nearest_x - self.x)
            return BehaviorTree.SUCCESS
        else:
            pass
        return BehaviorTree.FAIL


    def move_to_player(self):
        # fill here
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS
        pass

    def move_to_ball(self):
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()
        return BehaviorTree.SUCCESS

    def move_to_target(self):
        # fill here
        self.speed = RUN_SPEED_PPS
        self.calculate_current_position()

        distance = (self.target_x - self.x) ** 2 + (self.target_y - self.y) ** 2

        if distance < PIXEL_PER_METER ** 2:
            return BehaviorTree.SUCCESS
        else:
            return BehaviorTree.RUNNING
        pass

    def build_behavior_tree(self):
        # fill here
        root_node = SelectorNode('root')

        wander_node = LeafNode("Wander", self.wander)

        find_player_node = LeafNode("Find Player", self.find_player)
        move_to_player_node = LeafNode("Move to Player", self.move_to_player)

        find_ball_node = LeafNode("Find Ball", self.find_ball)
        move_to_ball_node = LeafNode("Move to Ball", self.move_to_ball)

        eat_ball_node = SequenceNode("Eat Ball")
        chase_node = SequenceNode("Chase")

        eat_ball_node.add_children(find_ball_node, move_to_ball_node)
        chase_node.add_children(find_player_node, move_to_player_node)

        root_node.add_children(chase_node,eat_ball_node,wander_node)
        self.bt = BehaviorTree(root_node)
        pass

    def get_bb(self):
        return self.x - 50, self.y - 50, self.x + 50, self.y + 50

    def update(self):
        # fill here
        self.bt.run()
        pass

    def draw(self):
        if math.cos(self.dir) < 0:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].composite_draw(0, 'h', self.x, self.y, 100, 100)
        else:
            if self.speed == 0:
                Zombie.images['Idle'][int(self.frame)].draw(self.x, self.y, 100, 100)
            else:
                Zombie.images['Walk'][int(self.frame)].draw(self.x, self.y, 100, 100)

        self.font.draw(self.x - 50, self.y + 60, '(HP : %2d)' % self.hp, (255, 255, 0))
        draw_rectangle(*self.get_bb())

    def handle_event(self, event):
        pass
