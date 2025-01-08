def q1():
    print('''**Определение**. Произведение матрицы $A$ размера $n×k$ и матрицы $B$ размера $k×m$– это матрица $C$ размера $n×m$ такая что её элементы записываются как $$c_{ij}=∑_{s=1}^{k}a_{is}b_{sj},i=1,…,n,j=1,…,m$$

Для $m=k=n$ сложность наивного алгоритма составляет $2n^3−n^2=O(n^3)$:

Почему рукописная(наивная) реализация такая медленная?

1) не используется параллелилизм

2) не используются преимущества быстрой памяти, в целом архитектуры памяти

**Определение**. Произведение матрицы $A$ размера $n×k$ и вектора $B$ размера $1×k$– это вектор $C$ длины $n$, такой, что его элементы записываются как $$c_{i}=∑_{j=1}^{k}a_{ij}b_{j},i=1,…,n$$''')
    
def q1_th():
    print('''def matmul(a, b): #наивное перемножение матриц
    n = a.shape[0]
    k = a.shape[1]
    m = b.shape[1]
    c = np.zeros((n, m))
    for i in range(n):
        for j in range(m):
            for s in range(k):
                c[i, j] += a[i, s] * b[s, j]
    return c


    def mat_vec_mult(matrix, vector): # Наивное перемножение матрицы на вектор
        num_rows = len(matrix)
        num_cols = len(matrix[0])
        result = [0] * num_rows

        for i in range(num_rows):
            for j in range(num_cols):
                result[i] += matrix[i,j] * vector[j]

        return result


    mat_vec_mult(np.array([[1,2],[2,3],[4,7]]),[4,5]), matmul(np.array([[1,2],[2,3]]),np.array([[1,2],[2,3]]))''')









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