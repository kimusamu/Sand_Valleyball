objects = [[] for _ in range(5)]
collision_pairs = {}


def add_object(o, depth = 0):
    objects[depth].append(o)

def add_objects(ol, depth = 0):
    objects[depth] += ol


def update():
    for layer in objects:
        for o in layer:
            o.update()


def render():
    for layer in objects:
        for o in layer:
            o.draw()

def add_collision_pair(group, a, b): #add_collision_pair('boy:ball', None, ball)
    if group not in collision_pairs: #dictionary에 키 group이 존재하지 않음
        print(f'New group {group} added')
        collision_pairs[group] = [ [], [] ]
    if a:
        collision_pairs[group][0].append(a)
    if b:
        collision_pairs[group][1].append(b)


def remove_collision_object(o):
    for pairs in collision_pairs.values():
        if o in pairs[0]:
            pairs[0].remove(o)
        if o in pairs[1]:
            pairs[1].remove(o)


def remove_object(o):
    for layer in objects:
        if o in layer:
            layer.remove(o)
            return
    raise ValueError('Cannot delete non existing object')


def clear():
    for layer in objects:
        layer.clear()

def collide(a, b):
    la, ba, ra, ta = a.get_bb()
    lb_1, bb_1, rb_1, tb_1 = b.get_bb_1()
    lb_2, bb_2, rb_2, tb_2 = b.get_bb_2()
    lb_3, bb_3, rb_3, tb_3 = b.get_bb_3()
    lb_4, bb_4, rb_4, tb_4 = b.get_bb_4()
    lb_5, bb_5, rb_5, tb_5 = b.get_bb_5()
    lb_6, bb_6, rb_6, tb_6 = b.get_bb_6()

    if la > rb_1 : return False
    if ra < lb_1 : return False
    if ta < bb_1 : return False
    if ba > tb_1 : return False

    if la > rb_2 : return False
    if ra < lb_2 : return False
    if ta < bb_2 : return False
    if ba > tb_2 : return False

    if la > rb_3 : return False
    if ra < lb_3 : return False
    if ta < bb_3 : return False
    if ba > tb_3 : return False

    if la > rb_4 : return False
    if ra < lb_4 : return False
    if ta < bb_4 : return False
    if ba > tb_4 : return False

    if la > rb_5 : return False
    if ra < lb_5 : return False
    if ta < bb_5 : return False
    if ba > tb_5 : return False

    if la > rb_6 : return False
    if ra < lb_6 : return False
    if ta < bb_6 : return False
    if ba > tb_6 : return False

    return True


def handle_collisions():
    for group, pairs in collision_pairs.items():
        for a in pairs[0]:
            for b in pairs[1]:
                if collide(a, b):
                    a.handle_collision(group, b)
                    b.handle_collision(group, a)