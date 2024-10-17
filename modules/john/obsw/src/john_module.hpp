#include "../../../../ps/inc/platform_services.hpp"

#include "../mission/john_version.hpp"
#include "../platform/john_msgids.hpp"
#include "../platform/john_platform.hpp"
#include "../platform/john_msg.hpp"

using namespace PlatformServices;

namespace Modules
{
class JohnModule : public ModuleMaker
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
    JohnModule();

    int32_t init(void);
    int32_t execute(void);
};
} // namespace Modules