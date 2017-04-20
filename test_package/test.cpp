#include <fmilib.h>
#include <stdio.h>
#include <iostream>

void importlogger(const jm_callbacks* c, const jm_string module,
                  const jm_log_level_enu_t log_level, const jm_string message) {
    printf("module = %s, log level = %d: %s\n", module, log_level, message);
}

int main() {
    jm_callbacks callbacks;

    callbacks.malloc = malloc;
    callbacks.calloc = calloc;
    callbacks.realloc = realloc;
    callbacks.free = free;
    callbacks.logger = importlogger;
    callbacks.log_level = jm_log_level_all;
    callbacks.context = 0;

    fmi_import_context_t* context = fmi_import_allocate_context(&callbacks);
    fmi_import_free_context(context);

    return 0;
}
