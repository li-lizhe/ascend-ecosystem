// Minimal driver that reproduces the libFuzzer return-value contract that every
// test/fuzzing/fuzz_*.cpp harness in apache/brpc violates when its size guard
// returns 1.
//
// libFuzzer only accepts 0 (input consumed) or -1 (input rejected) from
// LLVMFuzzerTestOneInput; it asserts `CBRes == 0 || CBRes == -1` after every call
// (compiler-rt/lib/fuzzer/FuzzerLoop.cpp:622), and its first input is the empty one.
#include <cassert>
#include <cstddef>
#include <cstdint>
#include <cstdio>

static const size_t kMinInputLength = 5;
static const size_t kMaxInputLength = 1024;

// Mirrors the guard at the top of every test/fuzzing/fuzz_*.cpp harness.
extern "C" int LLVMFuzzerTestOneInput(const uint8_t* data, size_t size) {
    (void)data;
    if (size < kMinInputLength || size > kMaxInputLength) {
#ifdef BEFORE_FIX
        return 1;
#else
        return 0;
#endif
    }
    return 0;
}

int main() {
    const uint8_t empty[1] = {0};
    // libFuzzer runs the empty input first, before any corpus entry.
    int r = LLVMFuzzerTestOneInput(empty, 0);
    printf("LLVMFuzzerTestOneInput(empty input) -> %d\n", r);
    // Verbatim from compiler-rt/lib/fuzzer/FuzzerLoop.cpp:622
    assert(r == 0 || r == -1);
    printf("return-value contract satisfied: CBRes=%d\n", r);
    return 0;
}
