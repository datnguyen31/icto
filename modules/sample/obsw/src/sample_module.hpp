#include "../../../../ps/inc/platform_services.hpp"

#include "../mission/sample_version.hpp"
#include "../platform/sample_msgids.hpp"
#include "../platform/sample_platform.hpp"

using namespace PlatformServices;

namespace Modules
{
class SampleModule : public ModuleMaker
{
  public:
    struct Housekeeping_t
    {
        uint32_t loopCtr;
    };

    Subscriber MsgPipe;
    Message    receivedMsg;
    Message    HkMsg;

  public:
    SampleModule();

    int32_t init(void);
    int32_t execute(void);
};
} // namespace Modules