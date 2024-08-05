#include "platform_services.hpp"

#include "sample_msgids.hpp"
#include "sample_platform.hpp"
#include "sample_version.hpp"

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