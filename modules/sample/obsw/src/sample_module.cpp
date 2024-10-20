#include "sample_module.hpp"

#include <iostream>

using namespace PlatformServices;

using namespace Modules;

SampleModule::SampleModule() : ModuleMaker(), HkMsg(0, "", nullptr, 0), receivedMsg(0, "", nullptr, 0)
{
    // Initialize housekeeping message
    HkMsg.header.messageId = SAMPLE_HOUSEKEEPING_MSGID;
    HkMsg.header.sender    = "SampleModule";
    HkMsg.data             = new Housekeeping_t;
    HkMsg.header.dataSize  = sizeof(Housekeeping_t);

    this->setState(ModuleState_t::MODULE_INITIALIZED);
}

SampleModule::SampleModule(const std::string moduleName, size_t queueSize) : ModuleMaker(moduleName, queueSize), HkMsg(0, "", nullptr, 0), receivedMsg(0, "", nullptr, 0)
{
    // Initialize housekeeping message
    HkMsg.header.messageId = SAMPLE_HOUSEKEEPING_MSGID;
    HkMsg.header.sender    = "SampleModule";
    HkMsg.data             = new Housekeeping_t;
    HkMsg.header.dataSize  = sizeof(Housekeeping_t);

    this->setState(ModuleState_t::MODULE_INITIALIZED);
}

int32_t SampleModule::init(void)
{
    // Subscribe to messages from Thread 2
    MsgPipe.subscribe(2);

    this->setState(ModuleState_t::MODULE_RUNNING);

    return 0;
}

int32_t SampleModule::execute(void)
{
    while (loopExamine() == ModuleState_t::MODULE_RUNNING)
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

#ifdef FOR_DEBUG
        std::cout << "SampleModule loopCtr: " << getLoopCtr() << std::endl;
#endif
    }

    return 0;
}

extern "C"
{
    void* SAMPLE_ChildTask(void* arg)
    {
        while(true)
        {
            std::cout << "Child task running" << std::endl;
            std::this_thread::sleep_for(std::chrono::seconds(1));
        }
    }
}

extern "C"
{
    void SAMPLE_ModuleEntry(void)
    {
        SampleModule sampleModule(SAMPLE_MODULE_NAME, SAMPLE_MODULE_PIPE_LENGTH);

        sampleModule.init();

        Executive &MissionExecutive = Executive::getInstance();
        MissionExecutive.createChildTask("SampleModule", SAMPLE_ChildTask, nullptr);
        
        sampleModule.execute();
    }
}