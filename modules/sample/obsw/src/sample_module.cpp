#include "sample_module.hpp"

#include <iostream>

using namespace PlatformServices;

using namespace Modules;

SampleModule::SampleModule() : loopCtr(0), MsgPipe(10), HkMsg(0, "", nullptr, 0), receivedMsg(0, "", nullptr, 0)
{
    // Initialize housekeeping message
    HkMsg.header.messageId = SAMPLE_HOUSEKEEPING_MSGID;
    HkMsg.header.sender    = "SampleModule";
    HkMsg.data             = new Housekeeping;
    HkMsg.header.dataSize  = sizeof(Housekeeping);

    // Initialize received message
    receivedMsg.header.messageId = 0;
    receivedMsg.header.sender    = "";
    receivedMsg.data             = nullptr;
    receivedMsg.header.dataSize  = 0;
}

int32_t SampleModule::init()
{
    // Subscribe to messages from Thread 2
    MsgPipe.subscribe(2);

    return 0;
}

int32_t SampleModule::execute()
{
    while (true)
    {
        if (MsgPipe.rcevMsg(receivedMsg, SAMPLE_MSG_DELAY_MS))
        { // Wait up to 1 second for a response
            switch (receivedMsg.header.messageId)
            {
                case 2:
                    // Process received message
                    break;
                default:
                    break;
            }
        }

#ifdef DEBUG_PRINT
        std::cout << "SampleModule loopCtr: " << loopCtr << std::endl;
#endif
        loopCtr++;
    }

    return 0;
}

extern "C"
{
    void SAMPLE_ModuleEntry(void)
    {
        SampleModule sampleModule;

        sampleModule.init();
        sampleModule.execute();
    }
}