def euler_func_code():
    print('''
    def euler(f, x_end, y0, N):
        h = x_end / N
        x = np.linspace(0.0, x_end, N+1)

        y = np.zeros((N+1, len(y0)))
        y[0,:] = y0
        for n in range(N):
              y[n+1, :] = y[n, :] + h*f(x[n], y[n,:])
        return x,y

    def simple(x,y):
          return -np.sin(x)

    x_5, y_5 = euler(simple, 0.5, [1.0], 5)
    x_50, y_50 = euler(simple, 0.5, [1.0], 50)

    print(f'Решение при х=0.5  и h = 0.1 -> {y_5[-1][0]}')
    print(f'Решение при х=0.05  и h = 0.1 -> {y_50[-1][0]}')
    print(f'Точное решение - {np.cos(0.5)}')''')