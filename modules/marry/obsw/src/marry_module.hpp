#include "../../../../ps/inc/platform_services.hpp"

#include "../mission/marry_version.hpp"
#include "../platform/marry_msgids.hpp"
#include "../platform/marry_platform.hpp"
#include "../platform/marry_msg.hpp"

using namespace PlatformServices;

namespace Modules
{
class MarryModule : public ModuleMaker
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
    MarryModule();

    int32_t init(void);
    int32_t execute(void);
};
} // namespace Modules