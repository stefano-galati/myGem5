#include "base/statistics.hh"

namespace gem5 {

    void fatal_stats_dump() {
        statistics::dump();
    }

}
