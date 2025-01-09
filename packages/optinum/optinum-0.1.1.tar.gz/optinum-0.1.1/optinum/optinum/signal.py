import numpy as np

def dft(x: np.ndarray[np.complex128]) -> np.ndarray[np.complex128]:
    """
    Вычисляет дискретное преобразование Фурье (ДПФ) входного сигнала.

    Функция реализует ДПФ, используя матричное умножение для эффективного вычисления.

    Параметры
    ----------
    x : np.ndarray[np.complex128]
        Входной сигнал как массив комплексных чисел

    Возвращает
    ----------
    np.ndarray[np.complex128]
        Результат ДПФ - массив комплексных чисел той же длины, что и входной сигнал

    Пример
    -------
    >>> x = np.array([1+0j, 2+0j, 3+0j, 4+0j])
    >>> dft(x)
    array([ 10.+0.j,  -2.+2.j,  -2.+0.j,  -2.-2.j])
    """
    N = len(x)
    n = np.arange(N)[:, None]  # Create a column vector of n
    k = np.arange(N)[None, :]  # Create a row vector of k
    W = np.exp(-2j * np.pi * k * n / N)  # Calculate the DFT matrix using broadcasting
    return x @ W

def idft(X: np.ndarray[np.complex128]) -> np.ndarray[np.complex128]:
    """
    Вычисляет обратное дискретное преобразование Фурье (ОДПФ) входного сигнала.

    Функция реализует ОДПФ, используя матричное умножение для эффективного вычисления.

    Параметры
    ----------
    X : np.ndarray[np.complex128]
        Входной сигнал как массив комплексных чисел

    Возвращает
    ----------
    np.ndarray[np.complex128]
        Результат ОДПФ - массив комплексных чисел той же длины, что и входной сигнал

    Пример
    -------
    >>> X = np.array([10+0j, -2+2j, -2+0j, -2-2j])
    >>> idft(X)
    array([ 1.+0.j,  2.+0.j,  3.+0.j,  4.+0.j])
    """
    N = len(X)
    n = np.arange(N)[:, None]  # Create a column vector of n
    k = np.arange(N)[None, :]  # Create a row vector of k
    W = np.exp(2j * np.pi * k * n / N)  # Calculate the IDFT matrix using broadcasting
    return X @ W / N

def fft(x: np.ndarray[np.complex128]) -> np.ndarray[np.complex128]:
    """
    Быстрое преобразование Фурье (БПФ) с использованием алгоритма Cooley-Tukey.
    
    Параметры:
    ----------
    x : np.ndarray[np.complex128]
        Входной массив комплексных чисел
        
    Возвращает:
    -----------
    np.ndarray[np.complex128]
        Результат БПФ
    """
    original_N = len(x)
    N = len(x)
    
    # Дополняем входной массив нулями до ближайшей степени двойки
    if N & (N-1) != 0:
        next_power_2 = 1 << (N - 1).bit_length()
        x = np.pad(x, (0, next_power_2 - N), mode='constant')
        N = next_power_2
    
    # Базовый случай рекурсии
    if N == 1:
        return x
    
    # Разделяем на четные и нечетные индексы
    even = fft(x[::2])
    odd = fft(x[1::2])
    
    # Вычисляем комплексные экспоненты
    factor = np.exp(-2j * np.pi * np.arange(N) / N)
    
    # Объединяем результаты по формуле X_k = E_k + e^(-2πik/N)O_k
    result = np.concatenate([
        even + factor[:N//2] * odd,      # Для k от 0 до N/2-1
        even + factor[N//2:] * odd       # Для k от N/2 до N-1
    ])
    
    # Возвращаем только нужное количество элементов
    return result[:original_N]

def ifft(X: np.ndarray[np.complex128]) -> np.ndarray[np.complex128]:
    """
    Обратное быстрое преобразование Фурье (ОБПФ) с использованием алгоритма Cooley-Tukey.
    
    Параметры:
    ----------
    X : np.ndarray[np.complex128]
        Входной массив комплексных чисел
        
    Возвращает:
    -----------
    np.ndarray[np.complex128]
        Результат ОБПФ
    """
    # Применяем БПФ к комплексно-сопряженным элементам
    result = np.conj(fft(np.conj(X))) / len(X)
    return result