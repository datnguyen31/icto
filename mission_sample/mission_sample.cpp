#include "../ps/inc/platform_services.hpp"

#include <iostream>
#include <thread>

using namespace PlatformServices;

int main()
{
    Executive MissionExecutive;

    // Load thread information from file
    if(!MissionExecutive.loadThreadsFromFile("mission_modules.txt"))
    {
        std::cerr << "Failed to load threads from file" << std::endl;
        return 0;
    }

    // Create and start both threads
    if(MissionExecutive.create("SampleModule"))
    {
        std::cout << "Thread1 created successfully" << std::endl;
    }
    else
    {
        std::cerr << "Failed to create Thread1" << std::endl;
    }

    while(1)
    {
        std::this_thread::sleep_for(std::chrono::seconds(1));
    }

    // Clean up
    MissionExecutive.destroyAll();

    return 0;
}