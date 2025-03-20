#include <iostream>

#include "register_fault_injector.hh"

namespace gem5 {

    RegisterFaultInjector::RegisterFaultInjector
        (const RegisterFaultInjectorParams &params) :
        SimObject(params),
        input_file(params.inputFile)   //initialization list
        {
            //std::cout << "Hello world, from a SimObject!" <<std::endl;
            std::cout << "Hey, I have a parameter: "
                << input_file << std::endl;
            std::cout << "Hey, I have a parameter: " << number << std::endl;
        }

    std::string RegisterFaultInjector::getString(void){
        return this->input_file;
    }

    int RegisterFaultInjector::getNumber(void){
        return this->number;
    }

}
