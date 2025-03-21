#ifndef __REGISTER_FAULT_INJECTOR_HH__
#define __REGISTER_FAULT_INJECTOR_HH__

#include "params/RegisterFaultInjector.hh"
#include "sim/sim_object.hh"

namespace gem5
{
    class RegisterFaultInjector : public SimObject
    {
        public:
            RegisterFaultInjector(const RegisterFaultInjectorParams &p);
            int getNumber(void);
            std::string getString(void);

            static std::string readFromFile(std::string filename);
            static std::vector<unsigned int>
                readMasks(std::string filename, int size);

        private:
            std::string input_file;
            int number;
    };
}

#endif //__REGISTER_FAULT_INJECTOR_HH__
