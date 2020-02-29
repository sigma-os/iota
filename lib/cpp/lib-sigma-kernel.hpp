#include <Sigma/types/vector.h>

namespace [[gnu::visibility("hidden")]] iota
{
    using index_type = uint8_t;

    template<typename T>
    using vector = types::vector<T>;

    template<typename T>
    vector<T> create_vector(){
        return {};
    }

    using string = types::vector<char>;

    string create_string(){
        return {};
    }
} // namespace iota