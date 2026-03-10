# Компилятор и флаги
CC = gcc
CFLAGS = -Wall -Wextra -std=c99 -O2
LDFLAGS = -lm

# Имя программы
TARGET = main.exe
SRC = main.c

# Сборка
all: $(TARGET)

$(TARGET): $(SRC)
	$(CC) $(CFLAGS) $(SRC) -o $(TARGET) $(LDFLAGS)
	@echo "Программа скомпилирована"

# Запуск
run: $(TARGET)
	$(TARGET)

# Очистка
clean:
	del $(TARGET)

# Тест для задачи 3
test3: $(TARGET)
	@echo "=== ТЕСТ ЗАДАЧИ 3 ==="
	echo 3 2 0 0 0 0 0 0 2 0 1 1 0 | $(TARGET)

.PHONY: all run clean test3