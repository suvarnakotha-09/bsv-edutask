describe("Todo Management Feature Tests", () => {

    let userId
    let userEmail
    let userName

    const openTaskDetails = () => {
        cy.contains("Automation Testing Task").click()
    }

    beforeEach(() => {

        cy.fixture("user.json").then((userData) => {

            cy.request({
                method: "POST",
                url: "http://localhost:5000/users/create",
                form: true,
                body: userData
            }).then((response) => {

                userId = response.body._id.$oid
                userEmail = userData.email
                userName = `${userData.firstName} ${userData.lastName}`

                cy.visit("http://localhost:3000")

                cy.contains("div", "Email Address")
                    .find("input[type=text]")
                    .type(userEmail)

                cy.get("form").submit()

                cy.get("h1")
                    .should(
                        "contain.text",
                        `Your tasks, ${userName}`
                    )

                cy.get(".submit-form")
                    .find("#title")
                    .type("Automation Testing Task")

                cy.get(".submit-form")
                    .find("#url")
                    .type("cZypFRdPS9M")

                cy.get('[type="submit"]').click()

                openTaskDetails()
            })
        })
    })

    context("R8UC1 - Create Todo Item", () => {

        it("should create a new todo item successfully", () => {

            cy.get('.inline-form > [type="text"]')
                .type("Practice Cypress testing")

            cy.get('.inline-form > [type="submit"]')
                .click()

            cy.get(".todo-item")
                .last()
                .should(
                    "contain.text",
                    "Practice Cypress testing"
                )
        })

        it("should keep add button disabled when description is empty", () => {

            cy.get('.inline-form > [type="submit"]')
                .should("be.disabled")
        })
    })

    context("R8UC2 - Toggle Todo Item", () => {

        it("should mark a todo item as completed", () => {

            cy.contains(".todo-list", "Watch video")
                .find(".checker")
                .click()

            cy.contains("Watch video")
                .should(
                    "have.css",
                    "text-decoration-line",
                    "line-through"
                )
        })

        it("should change a completed todo item back to active", () => {

            cy.contains(".todo-list", "Watch video")
                .find(".checker")
                .click()

            cy.contains("Watch video")
                .should(
                    "have.css",
                    "text-decoration-line",
                    "line-through"
                )

            cy.contains(".todo-list", "Watch video")
                .find(".checker")
                .click()

            cy.contains("Watch video")
                .should(($todo) => {
                    expect(
                        $todo.css("text-decoration-line")
                    ).to.not.equal("line-through")
                })
        })
    })

    context("R8UC3 - Delete Todo Item", () => {

        it("should delete an existing todo item", () => {

            cy.contains(".todo-list", "Watch video")
                .find(".remover")
                .click()

            cy.contains(".todo-list", "Watch video")
                .should("not.exist")
        })
    })

    afterEach(() => {

        cy.request({
            method: "DELETE",
            url: `http://localhost:5000/users/${userId}`
        })
    })
})

