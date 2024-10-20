#include "../../../../ps/inc/platform_services.hpp"

#include "../mission/sample_version.hpp"
#include "../platform/sample_msgids.hpp"
#include "../platform/sample_platform.hpp"
#include "../platform/sample_msg.hpp"

#define SAMPLE_MODULE_NAME "SampleModule"
#define SAMPLE_MODULE_PIPE_LENGTH 10

using namespace PlatformServices;

namespace Modules
{
class SampleModule : public ModuleMaker
{
  public:
    Message    receivedMsg;
    Message    HkMsg;

  public:
    SampleModule();
    SampleModule(const std::string moduleName, size_t queueSize);

    int32_t init(void);
    int32_t execute(void);
};
} // namespace Modules