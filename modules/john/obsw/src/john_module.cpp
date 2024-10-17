#include "john_module.hpp"

#include <iostream>

using namespace PlatformServices;

using namespace Modules;

JohnModule::JohnModule() : MsgPipe(10), HkMsg(0, "", nullptr, 0), receivedMsg(0, "", nullptr, 0)
{
    // Initialize housekeeping message
    HkMsg.header.messageId = JOHN_HOUSEKEEPING_MSGID;
    HkMsg.header.sender    = "JohnModule";
    HkMsg.data             = new Housekeeping_t;
    HkMsg.header.dataSize  = sizeof(Housekeeping_t);

    this->setState(ModuleState_t::MODULE_INITIALIZED);
}

int32_t JohnModule::init(void)
{
    // Subscribe to messages from Thread 2
    MsgPipe.subscribe(0xB1);

    this->setState(ModuleState_t::MODULE_RUNNING);

    return 0;
}

int32_t JohnModule::execute(void)
{

    while (loopExamine() == ModuleState_t::MODULE_RUNNING)
    {
        if (MsgPipe.rcevMsg(receivedMsg, JOHN_MSG_DELAY_MS))
        { // Wait up to 1 second for a response
            if (receivedMsg.header.messageId == 0xB1)
            {
                std::cout << "JohnModule received message from Marry" << std::endl;
                ts.sleepFor(1,0);

                john_msg_t msg;
                msg.a = 1;
                msg.b = 2;

                Message JohnMsg(JOHN_CUSTOM_MSGID, "JohnModule", &msg, sizeof(john_msg_t));

                // Send message to Marry
                MsgPipe.sendMsg(JohnMsg);
            }
            else
            {
                std::cout << "JohnModule received unknown messageId" << std::endl;
            }
        }

#ifdef FOR_DEBUG
        std::cout << "JohnModule loopCtr: " << getLoopCtr() << std::endl;
#endif
    }

    return 0;
}

extern "C"
{
    void JOHN_ModuleEntry(void)
    {
        JohnModule johnModule;

        johnModule.init();
        johnModule.execute();
    }
}