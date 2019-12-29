#include <optional>
#include <vector>
#include <string>

namespace iota
{
    using index_type = uint8_t;

    template<typename T>
    using optional = std::optional<T>;

    template<typename T>
    optional<T> create_optional(){
        return {};
    }

    template<typename T>
    using vector = std::vector<T>;

    template<typename T>
    vector<T> create_vector(){
        return {};
    }

    using string = std::string;

    string create_string(){
        return {};
    }
} // namespace iota