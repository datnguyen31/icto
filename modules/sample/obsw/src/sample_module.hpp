#include "../../../../ps/inc/platform_services.hpp"

#include "../mission/sample_version.hpp"
#include "../platform/sample_msgids.hpp"
#include "../platform/sample_platform.hpp"
#include "../platform/sample_msg.hpp"

using namespace PlatformServices;

namespace Modules
{
class SampleModule : public ModuleMaker
{
  public:
    Subscriber MsgPipe;
    Message    receivedMsg;
    Message    HkMsg;

  public:
    SampleModule();

    int32_t init(void);
    int32_t execute(void);
};
} // namespace Modules