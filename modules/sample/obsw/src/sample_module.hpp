#include "../../../../ps/inc/platform_services.hpp"

#include "../platform/sample_msgids.hpp"
#include "../platform/sample_platform.hpp"
#include "../mission/sample_version.hpp"

#include <stdint.h>

using namespace PlatformServices;

namespace Modules
{
class SampleModule
{
    public:
    struct Housekeeping
    {
        uint32_t loopCtr;
    };

    Subscriber MsgPipe;
    Message    receivedMsg;
    Message    HkMsg;
    uint32_t   loopCtr;

    public:
    SampleModule();

    int32_t init();
    int32_t execute();
};
} // namespace Modules