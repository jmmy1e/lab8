"""
LAB #8
    10/15/2025
    Student 1: Jimmy Le
    Student 2: Daniel McCray

    Rad Racer: Simple three-lane racing game using abstract classes and inheritance.
    The user picks a vehicle and races the other two to the finish.
"""
import random
from check_input import get_int_range
from car import Car
from motorcycle import Motorcycle
from truck import Truck

LANES = 3
LENGTH = 100  # columns per lane

def make_track():
    """Builds a blank 3x100 track as a list of lists filled with '-'."""
    track = []
    r = 0
    while r < LANES:
        row = []
        c = 0
        while c < LENGTH:
            row.append('-')
            c = c + 1
        track.append(row)
        r = r + 1
    return track

def place_obstacles(track):
    """Places two '0' obstaclkes in each lane (not at the start or end)."""
    r = 0
    while r < LANES:
        placed = 0
        while placed < 2:
            col = random.randint(1, LENGTH - 2)
            if track[r][col] == '-':
                track[r][col] = '0'
                placed = placed + 1
        r = r + 1

def next_obstacle(row, current_pos):
    """Return the index of the next '0' after current_pos, or None if there isn't one."""
    start = current_pos + 1
    i = start
    while i < LENGTH:
        if row[i] == '0':
            return i
        i = i + 1
    return None

def draw_move(track, lane, old_pos, new_pos, ch):
    """Mark the old position with '*' and the new position with the vehicle letter."""
    if old_pos >= 0 and old_pos < LENGTH:
        track[lane][old_pos] = '*'
    if new_pos >= LENGTH:
        new_pos = LENGTH - 1
    if new_pos < 0:
        new_pos = 0
    track[lane][new_pos] = ch

def print_status_then_track(track, vehicles):
    """Print each vehicle's status line, then print the three lanes."""
    i = 0
    while i < len(vehicles):
        print(vehicles[i])
        i = i + 1
    r = 0
    while r < LANES:
        print("".join(track[r]))
        r = r + 1

def ordinal(n):
    """Return a place label (1st, 2nd, 3rd)."""
    if n == 1:
        return "1st"
    elif n == 2:
        return "2nd"
    else:
        return "3rd"

def main():
    """
    Run a single race.
    Sets up the track and vehicles, prompts the player for moves each round,
    Randomly pick moves for the other two vehicles, and prints the results.
    After the player finishes, the game auto-plays the rest to show the final order.
    """
    print("Rad Racer!")
    print("Choose a vehicle and race it down the track (player = 'P').  Slow down for obstacles ('0') or else you'll crash!")
    print("1. Lightning Car - a fast car. Speed: 7.  Special: Nitro Boost (1.5x speed)")
    print("2. Swift Bike - a speedy motorcycle. Speed: 8.  Special: Wheelie (2x speed but there's a chance you'll wipe out).")
    print("3. Behemoth Truck - a heavy truck. Speed: 6.  Special: Ram (2x speed and it smashes through obstacles).")

    track = make_track()
    place_obstacles(track)

    # Choose vehicle
    choice = get_int_range("Choose your vehicle (1-3): ", 1, 3)

    car = Car("Lightning Car", 'C', 7)
    moto = Motorcycle("Swift Bike", 'M', 8)
    truck = Truck("Behemoth Truck", 'T', 6)

    vehicles = [car, moto, truck]
    initials = ['C', 'M', 'T']
    player_idx = choice - 1

    # initials at start; player labeled 'P'
    lane = 0
    while lane < LANES:
        track[lane][0] = initials[lane]
        lane = lane + 1
    track[player_idx][0] = 'P'

    finished_order = []

    # show initial status + track once before the loop
    print_status_then_track(track, vehicles)

    running = True
    while running:
        # player turn
        if (player_idx not in finished_order) and (vehicles[player_idx].position < LENGTH - 1):
            action = get_int_range("Choose action (1. Fast, 2. Slow, 3. Special Move): ", 1, 3)

            v = vehicles[player_idx]
            lane = player_idx
            row = track[lane]
            obs = next_obstacle(row, v.position)
            before = v.position

            if action == 1:
                msg = v.fast(obs)
            elif action == 2:
                msg = v.slow(obs)
            else:
                msg = v.special_move(obs)

            print("")          # single blank line before event text
            print(msg)

            draw_move(track, lane, before, v.position, 'P')

            # --- clamp after move (player) ---
            if v.position >= LENGTH - 1:
                v.position = LENGTH - 1
            # ---------------------------------

            if v.position >= LENGTH - 1 and player_idx not in finished_order:
                finished_order.append(player_idx)

            # autoplay if player finished
            if player_idx in finished_order:
                while len(finished_order) < 3:
                    print("")  # blank line BEFORE opponents' messages

                    i = 0
                    while i < len(vehicles):
                        if i != player_idx:
                            opp = vehicles[i]
                            if (i not in finished_order) and (opp.position < LENGTH - 1):
                                lane = i
                                row = track[lane]
                                obs = next_obstacle(row, opp.position)
                                before = opp.position

                                if opp.energy <= 0:
                                    om = opp.slow(obs)
                                else:
                                    rnum = random.random()
                                    if rnum < 0.40:
                                        om = opp.slow(obs)
                                    elif rnum < 0.70:
                                        om = opp.fast(obs)
                                    else:
                                        om = opp.special_move(obs)
                                print(om)
                                draw_move(track, lane, before, opp.position, initials[i])

                                # --- clamp after move (autoplay opponents) ---
                                if opp.position >= LENGTH - 1:
                                    opp.position = LENGTH - 1
                                # ---------------------------------------------

                                if opp.position >= LENGTH - 1 and i not in finished_order:
                                    finished_order.append(i)
                        i = i + 1

                    print("")  # blank line before statuses
                    print_status_then_track(track, vehicles)
                break

        # OPPONENTS (normal round)
        i = 0
        while i < len(vehicles):
            if i != player_idx:
                v = vehicles[i]
                if (i not in finished_order) and (v.position < LENGTH - 1):
                    lane = i
                    row = track[lane]
                    obs = next_obstacle(row, v.position)
                    before = v.position

                    if v.energy <= 0:
                        msg = v.slow(obs)
                    else:
                        rnum = random.random()
                        if rnum < 0.40:
                            msg = v.slow(obs)
                        elif rnum < 0.70:
                            msg = v.fast(obs)
                        else:
                            msg = v.special_move(obs)
                    print(msg)
                    draw_move(track, lane, before, v.position, initials[i])

                    # --- clamp after move (normal opponents) ---
                    if v.position >= LENGTH - 1:
                        v.position = LENGTH - 1
                    # -------------------------------------------

                    if v.position >= LENGTH - 1 and i not in finished_order:
                        finished_order.append(i)
            i = i + 1

        print("")  # blank line before statuses
        print_status_then_track(track, vehicles)

        if len(finished_order) == 3:
            running = False

    # Results
    print("1st place: " + str(vehicles[finished_order[0]]))
    print("2nd place: " + str(vehicles[finished_order[1]]))
    print("3rd place: " + str(vehicles[finished_order[2]]))

if __name__ == "__main__":
    main()