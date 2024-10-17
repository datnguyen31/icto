#include "marry_module.hpp"

#include <iostream>

using namespace PlatformServices;

using namespace Modules;

MarryModule::MarryModule() : MsgPipe(10), HkMsg(0, "", nullptr, 0), receivedMsg(0, "", nullptr, 0)
{
    // Initialize housekeeping message
    HkMsg.header.messageId = MARRY_HOUSEKEEPING_MSGID;
    HkMsg.header.sender    = "MarryModule";
    HkMsg.data             = new Housekeeping_t;
    HkMsg.header.dataSize  = sizeof(Housekeeping_t);

    this->setState(ModuleState_t::MODULE_INITIALIZED);
}

int32_t MarryModule::init(void)
{
    // Subscribe to messages from Thread 2
    MsgPipe.subscribe(0xA1);

    this->setState(ModuleState_t::MODULE_RUNNING);

    return 0;
}

int32_t MarryModule::execute(void)
{
    Message toJohn(0xB1, "MarryModule", nullptr, 0);
    MsgPipe.sendMsg(toJohn);

    while (loopExamine() == ModuleState_t::MODULE_RUNNING)
    {
        if (MsgPipe.rcevMsg(receivedMsg, MARRY_MSG_DELAY_MS))
        { // Wait up to 1 second for a response
            if(receivedMsg.header.messageId == 0xA1)
            {
                std::cout << "MarryModule received message from John" << std::endl;
                ts.sleepFor(1,0);
                // Send message to John
                john_send_msg_t msg;
                msg.a = 3;
                msg.b = 4;
                Message JohnMsg(MARRY_CUSTOM_MSGID, "MarryModule", &msg, sizeof(john_send_msg_t));
                MsgPipe.sendMsg(JohnMsg);
            }
            else
            {
                std::cout << "MarryModule received unknown messageId" << std::endl;
            }
        }

#ifdef FOR_DEBUG
        std::cout << "MarryModule loopCtr: " << getLoopCtr() << std::endl;
#endif
    }

    return 0;
}

extern "C"
{
    void MARRY_ModuleEntry(void)
    {
        MarryModule marryModule;

        marryModule.init();
        marryModule.execute();
    }
}