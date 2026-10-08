CC      = gcc
BIN     = bin
PT_SRC  = $(wildcard src/pthreads/*.c)
OMP_SRC = $(wildcard src/openmp/*.c)
PT_BIN  = $(patsubst src/pthreads/%.c,$(BIN)/%,$(PT_SRC))
OMP_BIN = $(patsubst src/openmp/%.c,$(BIN)/%,$(OMP_SRC))

all: $(BIN) $(PT_BIN) $(OMP_BIN) $(BIN)/sequential $(BIN)/pthread_perf $(BIN)/omp_perf

$(BIN):
	mkdir -p $(BIN)

$(BIN)/%: src/pthreads/%.c | $(BIN)
	$(CC) $< -o $@ -pthread

$(BIN)/%: src/openmp/%.c | $(BIN)
	$(CC) $< -o $@ -fopenmp

$(BIN)/sequential: src/performance/sequential.c | $(BIN)
	$(CC) $< -o $@

$(BIN)/pthread_perf: src/performance/pthread_perf.c | $(BIN)
	$(CC) $< -o $@ -pthread

$(BIN)/omp_perf: src/performance/omp_perf.c | $(BIN)
	$(CC) $< -o $@ -fopenmp

bench: all
	./scripts/run_benchmarks.sh

plots:
	python3 scripts/plot_results.py

clean:
	rm -rf $(BIN)

.PHONY: all bench plots clean
