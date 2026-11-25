using Documenter
using DocumenterLandingPage

const repo = dirname(@__DIR__)
const pages = ["index.md"; sort([joinpath("docs", f) for f in readdir(@__DIR__)
                                 if endswith(f, ".md")]);
               "reports/status.md"; "refuted/README.md"; "upstream-bugs.md"]
sourcefile(page) = page == "index.md" ? joinpath(repo, "README.md") : joinpath(repo, page)

# Stage the sources so generated files cannot be consumed by the next build.
mktempdir() do source
    for page in pages
        dest = joinpath(source, page)
        mkpath(dirname(dest))
        cp(sourcefile(page), dest)
    end
    cp(joinpath(repo, "reports", "numerical.json"), joinpath(source, "reports", "numerical.json"))
    mkpath(joinpath(source, "examples"))
    cp(joinpath(repo, "examples", "matrix-identities.json"), joinpath(source, "examples", "matrix-identities.json"))
    makedocs(;
        root = @__DIR__,
        source,
        build = joinpath(@__DIR__, "build"),
        sitename = "OpenSymbolicRules — LinearAlgebra",
        repo = Remotes.GitHub("OpenSymbolicRules", "LinearAlgebra"),
        remotes = nothing,
        plugins = [LandingPage()],
        pages,
        format = Documenter.HTML(; edit_link = nothing, prettyurls = false,
            repolink = "https://github.com/OpenSymbolicRules/LinearAlgebra",
            inventory_version = "0.1.0"),
    )
end

open(joinpath(@__DIR__, "build", "llms.txt"), "w") do io
    println(io, "# OpenSymbolicRules — LinearAlgebra\n")
    for page in pages
        title = replace(first(split(read(sourcefile(page), String), '\n')), r"^#+\s*" => "")
        println(io, "- [", title, "](", replace(page, ".md" => ".html"), ")")
    end
end
open(joinpath(@__DIR__, "build", "llms-full.txt"), "w") do io
    for page in pages
        println(io, read(sourcefile(page), String), "\n")
    end
end
