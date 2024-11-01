while True:
    try:
        X = int(input())
        N = int(input())

        lst = []
        for _ in range(N):
            lst.append(int(input()))
        lst.sort()
        start = 0
        end = N - 1
        is_possible = 'danger'
        while start < end:
            if lst[start] + lst[end] == X:
                is_possible = 'yes'
                break

            if lst[start] + lst[end] < X:
                start += 1
            elif lst[start] + lst[end] > X:
                # start = 0
                end -= 1

        if is_possible == 'danger':
            print('danger')
        else:
            print(f'{is_possible} {lst[start]} {lst[end]}')
    except:
        break