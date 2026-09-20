import sys, heapq

D = [(0, 1), (1, 0), (0, -1), (-1, 0)]

def read_state():
    while True:
        line = sys.stdin.readline()
        if not line:
            sys.exit(0)
        p = line.split()
        if len(p) >= 5:
            return list(map(int, p[:5]))

def main():
    H = {}
    visited = set()
    x = y = 0
    d = 0

    def observe(vals):
        cur, f, b, l, r = vals
        H[(x, y)] = cur
        visited.add((x, y))
        for off, v in ((0, f), (2, b), (3, l), (1, r)):
            dd = (d + off) % 4
            H.setdefault((x + D[dd][0], y + D[dd][1]), v)

    def plan():
        start = (x, y, d)
        dist = {start: 0}
        prev = {}
        pq = [(0, start)]

        while pq:
            c, s = heapq.heappop(pq)
            if dist.get(s, 1 << 30) < c:
                continue

            sx, sy, sd = s
            if (sx, sy) not in visited:
                continue

            moves = [
                ("RL", (sx, sy, (sd + 3) % 4)),
                ("RR", (sx, sy, (sd + 1) % 4)),
            ]

            for cmd, sign in (("FW", 1), ("BW", -1)):
                nx = sx + sign * D[sd][0]
                ny = sy + sign * D[sd][1]

                if (nx, ny) in H and abs(H[(nx, ny)] - H[(sx, sy)]) <= 1:
                    moves.append((cmd, (nx, ny, sd)))

            for cmd, ns in moves:
                nc = c + 1
                if nc < dist.get(ns, 1 << 30):
                    dist[ns] = nc
                    prev[ns] = (s, cmd)
                    heapq.heappush(pq, (nc, ns))

        best = None

        for s, c in dist.items():
            cell = (s[0], s[1])

            if cell in visited:
                continue

            key = (-H[cell], c)

            if best is None or key < best[0]:
                best = (key, s)

        if best is None:
            return None, None

        s = best[1]
        cmds = []

        while s != start:
            s, cmd = prev[s]
            cmds.append(cmd)

        cmds.reverse()

        return H[(best[1][0], best[1][1])], cmds

    observe(read_state())

    while True:
        target_h, cmds = plan()

        if cmds is None or target_h < H[(x, y)]:
            print("SNP", flush=True)
            return

        for cmd in cmds:
            print(cmd, flush=True)

            if cmd == "RL":
                d = (d + 3) % 4
            elif cmd == "RR":
                d = (d + 1) % 4
            elif cmd == "FW":
                x += D[d][0]
                y += D[d][1]
            else:
                x -= D[d][0]
                y -= D[d][1]

            observe(read_state())

main()
